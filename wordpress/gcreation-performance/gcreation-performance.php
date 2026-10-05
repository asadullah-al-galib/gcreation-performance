<?php
/**
 * Plugin Name: gCreation Performance Doctor
 * Description: Evidence-backed performance scans, WooCommerce audits and secure Fix Center.
 * Version: 0.1.0
 * Requires PHP: 7.3
 */
if (!defined('ABSPATH')) { exit; }
if (file_exists(__DIR__ . '/config.php')) { require_once __DIR__ . '/config.php'; }

function gcp_engine($path, $data = null, $method = 'GET') {
    if (!defined('GCREATION_ENGINE_SECRET')) { return new WP_Error('gcp_config', 'The DEV audit service is not configured.'); }
    if (!preg_match('#^/[a-zA-Z0-9/_-]+(?:\?after=[0-9]+)?$#', $path)) { return new WP_Error('gcp_path', 'Invalid engine path.'); }
    $response = wp_remote_request('http://127.0.0.1:3101' . $path, array('method' => $method, 'timeout' => 20, 'redirection' => 0, 'headers' => array('X-Engine-Secret' => GCREATION_ENGINE_SECRET, 'Content-Type' => 'application/json'), 'body' => $data === null ? null : wp_json_encode($data)));
    if (is_wp_error($response)) { return $response; }
    $code = wp_remote_retrieve_response_code($response);
    $body = json_decode(wp_remote_retrieve_body($response), true);
    if ($code < 200 || $code >= 300) { return new WP_Error('gcp_engine', isset($body['error']) ? $body['error'] : 'Audit service unavailable.', array('status' => $code)); }
    return $body;
}
function gcp_permission($request) {
    return wp_verify_nonce($request->get_header('X-WP-Nonce'), 'wp_rest') ? true : new WP_Error('gcp_nonce', 'Refresh the page and try again.', array('status' => 403));
}
function gcp_limit($bucket, $maximum) {
    // REMOTE_ADDR only: do not trust browser-supplied forwarding headers.
    $key = 'gcp_rate_' . hash('sha256', $bucket . '|' . (isset($_SERVER['REMOTE_ADDR']) ? $_SERVER['REMOTE_ADDR'] : 'unknown'));
    $count = (int) get_transient($key);
    if ($count >= $maximum) { return false; }
    set_transient($key, $count + 1, HOUR_IN_SECONDS);
    return true;
}
function gcp_session() {
    $cookie = isset($_COOKIE['gcp_session']) ? $_COOKIE['gcp_session'] : '';
    if (!preg_match('/^[a-f0-9]{64}$/', $cookie)) { return ''; }
    return hash('sha256', $cookie);
}
function gcp_owns_scan($id) {
    return preg_match('/^[a-f0-9-]{36}$/', $id) && gcp_session() && hash_equals((string) get_transient('gcp_scan_' . $id), gcp_session());
}
add_action('rest_api_init', function () {
    register_rest_route('gcreation-performance/v1', '/scan', array('methods' => 'POST', 'permission_callback' => 'gcp_permission', 'callback' => function ($request) {
        if (!gcp_session()) { return new WP_Error('gcp_session', 'Enable cookies and refresh this page.', array('status' => 403)); }
        if (!gcp_limit('scan', 5)) { return new WP_Error('gcp_limit', 'Scan limit reached. Please try later.', array('status' => 429)); }
        $url = esc_url_raw((string) $request->get_param('url'), array('http', 'https'));
        if (!$url) { return new WP_Error('gcp_url', 'Enter a valid public URL.', array('status' => 400)); }
        $result = gcp_engine('/audits', array('url' => $url), 'POST');
        if (!is_wp_error($result)) { set_transient('gcp_scan_' . $result['id'], gcp_session(), DAY_IN_SECONDS); }
        return $result;
    }));
    register_rest_route('gcreation-performance/v1', '/scan/(?P<id>[a-f0-9-]{36})', array('methods' => 'GET', 'permission_callback' => 'gcp_permission', 'callback' => function ($request) {
        if (!gcp_owns_scan($request['id'])) { return new WP_Error('gcp_owner', 'Scan session required.', array('status' => 403)); }
        return gcp_engine('/audits/' . $request['id']);
    }));
    register_rest_route('gcreation-performance/v1', '/events/(?P<id>[a-f0-9-]{36})', array('methods' => 'GET', 'permission_callback' => 'gcp_permission', 'callback' => function ($request) {
        if (!gcp_owns_scan($request['id'])) { return new WP_Error('gcp_owner', 'Scan session required.', array('status' => 403)); }
        return gcp_engine('/audits/' . $request['id'] . '/events?after=' . absint($request->get_param('after')));
    }));
    register_rest_route('gcreation-performance/v1', '/analytics', array('methods' => 'POST', 'permission_callback' => 'gcp_permission', 'callback' => function ($request) {
        $id = sanitize_text_field((string) $request->get_param('auditId'));
        if (!gcp_owns_scan($id)) { return new WP_Error('gcp_owner', 'Scan session required.', array('status' => 403)); }
        return gcp_engine('/analytics', array('auditId' => $id, 'type' => 'free.report_viewed'), 'POST');
    }));
    register_rest_route('gcreation-performance/v1', '/quote', array('methods' => 'POST', 'permission_callback' => 'gcp_permission', 'callback' => function ($request) {
        $id = sanitize_text_field((string) $request->get_param('auditId'));
        if (!gcp_owns_scan($id)) { return new WP_Error('gcp_owner', 'Scan session required.', array('status' => 403)); }
        return gcp_engine('/quotes', array('auditId' => $id, 'scope' => sanitize_key((string) $request->get_param('scope')), 'mode' => sanitize_key((string) $request->get_param('mode'))), 'POST');
    }));
    register_rest_route('gcreation-performance/v1', '/expert-review', array('methods' => 'POST', 'permission_callback' => 'gcp_permission', 'callback' => function ($request) {
        $id = sanitize_text_field((string) $request->get_param('auditId'));
        if (!gcp_owns_scan($id) || !gcp_limit('expert', 5)) { return new WP_Error('gcp_owner', 'Scan session or request limit reached.', array('status' => 403)); }
        $contact = sanitize_email((string) $request->get_param('contact'));
        $result = gcp_engine('/expert/review', array('auditId' => $id, 'contact' => $contact), 'POST');
        if (!is_wp_error($result)) { add_option('gcp_expert_contact_' . $result['id'], $contact, '', false); }
        return $result;
    }));
    register_rest_route('gcreation-performance/v1', '/checkout', array('methods' => 'POST', 'permission_callback' => 'gcp_permission', 'callback' => 'gcp_checkout'));
    register_rest_route('gcreation-performance/v1', '/report', array('methods' => 'POST', 'permission_callback' => 'gcp_permission', 'callback' => function ($request) {
        if (!gcp_limit('verify', 30)) { return new WP_Error('gcp_limit', 'Verification limit reached.', array('status' => 429)); }
        $action = sanitize_key((string) $request->get_param('action'));
        if (!in_array($action, array('', 'fixed', 'retest', 'expert'), true)) { return new WP_Error('gcp_action', 'Invalid action.', array('status' => 400)); }
        return gcp_engine('/reports/access', array('token' => (string) $request->get_param('token'), 'orderId' => (string) absint($request->get_param('orderId')), 'contact' => sanitize_email((string) $request->get_param('contact')), 'action' => $action, 'ruleId' => sanitize_key((string) $request->get_param('ruleId')), 'url' => esc_url_raw((string) $request->get_param('url'))), 'POST');
    }));
});
add_action('init', function () {
    if (is_admin() || isset($_COOKIE['gcp_session']) || headers_sent()) { return; }
    $cookie = bin2hex(random_bytes(32));
    setcookie('gcp_session', $cookie, array('expires' => time() + DAY_IN_SECONDS, 'path' => '/', 'secure' => is_ssl(), 'httponly' => true, 'samesite' => 'Lax'));
    $_COOKIE['gcp_session'] = $cookie;
});
function gcp_checkout($request) {
    if (function_exists('WC') && !WC()->cart && function_exists('wc_load_cart')) { wc_load_cart(); }
    if (!function_exists('WC') || !WC()->cart) { return new WP_Error('gcp_wc', 'WooCommerce checkout is unavailable.', array('status' => 503)); }
    $id = sanitize_text_field((string) $request->get_param('auditId'));
    if (!gcp_owns_scan($id)) { return new WP_Error('gcp_owner', 'Scan session required.', array('status' => 403)); }
    $scope = sanitize_key((string) $request->get_param('scope')); $mode = sanitize_key((string) $request->get_param('mode'));
    $quote = gcp_engine('/quotes', array('auditId' => $id, 'scope' => $scope, 'mode' => $mode), 'POST');
    if (is_wp_error($quote)) { return $quote; }
    if ($quote['amount'] === null) { return new WP_Error('gcp_custom', 'This website needs a custom expert review.', array('status' => 409)); }
    if (get_woocommerce_currency() !== $quote['currency']) { return new WP_Error('gcp_currency', 'DEV store currency must match the configured BDT pricing.', array('status' => 409)); }
    $product = (int) get_option('gcp_product_id');
    if (!$product || !wc_get_product($product)) { return new WP_Error('gcp_product', 'Create the audit product in Performance Doctor Settings.', array('status' => 503)); }
    if (!WC()->cart->add_to_cart($product, 1, 0, array(), array('gcp' => array('auditId' => $id, 'scope' => $scope, 'mode' => $mode, 'quote' => $quote)))) { return new WP_Error('gcp_cart', 'Could not add audit to checkout.', array('status' => 409)); }
    return array('checkoutUrl' => wc_get_checkout_url());
}
add_action('woocommerce_before_calculate_totals', function ($cart) {
    foreach ($cart->get_cart() as $key => $item) {
        if (empty($item['gcp'])) { continue; }
        $data = $item['gcp'];
        $quote = gcp_engine('/quotes', array('auditId' => $data['auditId'], 'scope' => $data['scope'], 'mode' => $data['mode']), 'POST');
        if (is_wp_error($quote) || $quote['amount'] === null || $quote['currency'] !== get_woocommerce_currency()) {
            $cart->remove_cart_item($key); wc_add_notice('The audit quote is unavailable. Run the package selection again.', 'error'); continue;
        }
        $item['data']->set_price($quote['amount']); $cart->cart_contents[$key]['gcp']['quote'] = $quote;
    }
});
add_action('woocommerce_checkout_create_order_line_item', function ($item, $key, $values) {
    if (empty($values['gcp'])) { return; }
    $data = $values['gcp'];
    $item->add_meta_data('_gcp_selection', $data, true);
    foreach (array('Audit ID' => $data['auditId'], 'Website URL' => $data['quote']['websiteUrl'], 'Analysis Scope' => $data['scope'], 'Detected URL Count' => $data['quote']['count'], 'Pricing Tier' => $data['quote']['tier'], 'Solution Mode' => $data['mode'], 'Report State' => 'Awaiting payment') as $label => $value) { $item->add_meta_data($label, $value, true); }
}, 10, 3);
function gcp_paid_order($order_id) {
    $order = wc_get_order($order_id);
    if (!$order || !$order->is_paid()) { return; }
    $attempts = (int) $order->get_meta('_gcp_sync_attempts');
    if ($attempts >= 3) { return; }
    $order->update_meta_data('_gcp_sync_attempts', $attempts + 1); $order->save();
    foreach ($order->get_items() as $item) {
        $data = $item->get_meta('_gcp_selection'); if (!$data || $item->get_meta('_gcp_paid_audit')) { continue; }
        $token = $item->get_meta('_gcp_report_token'); if (!$token) { $token_key = 'gcp_order_token_' . (int) $order_id; add_option($token_key, bin2hex(random_bytes(32)), '', false); $token = get_option($token_key); $item->update_meta_data('_gcp_report_token', $token); $item->save(); }
        $result = gcp_engine('/orders/paid', array('wcOrderId' => (string) $order_id, 'auditId' => $data['auditId'], 'scope' => $data['scope'], 'mode' => $data['mode'], 'contact' => $order->get_billing_email(), 'reportToken' => $token, 'amount' => (int) round($item->get_total()), 'currency' => $order->get_currency()), 'POST');
        if (is_wp_error($result)) { $order->add_order_note('Performance Doctor: paid audit synchronization requires retry.'); if (!wp_next_scheduled('gcp_retry_paid', array($order_id))) { wp_schedule_single_event(time() + 60, 'gcp_retry_paid', array($order_id)); } continue; }
        $item->update_meta_data('_gcp_paid_audit', $result['auditId']); $item->update_meta_data('Report State', 'Queued'); $item->save();
    }
}
add_action('woocommerce_payment_complete', 'gcp_paid_order');
add_action('woocommerce_order_status_processing', 'gcp_paid_order');
add_action('woocommerce_order_status_completed', 'gcp_paid_order');
add_action('gcp_retry_paid', 'gcp_paid_order');
add_action('woocommerce_thankyou', function ($order_id) {
    $order = wc_get_order($order_id); if (!$order) { return; }
    $key = isset($_GET['key']) ? sanitize_text_field(wp_unslash($_GET['key'])) : '';
    if (!hash_equals($order->get_order_key(), $key) && (!$order->get_user_id() || (int) get_current_user_id() !== (int) $order->get_user_id())) { return; }
    foreach ($order->get_items() as $item) {
        $token = $item->get_meta('_gcp_report_token'); if (!$token) { continue; }
        // Fragment is never sent in HTTP requests. Order/contact still required.
        $link = home_url('/performance-doctor/') . '#report=' . rawurlencode($token);
        echo '<p><a href="' . esc_url($link) . '">Open your secure Fix Center</a>. Verify with your order number and checkout email.</p>';
    }
});
add_shortcode('gcreation_performance', function () {
    wp_enqueue_script('gcp-app', plugins_url('app.js', __FILE__), array(), '0.1.0', true);
    wp_enqueue_style('gcp-app', plugins_url('app.css', __FILE__), array(), '0.1.0');
    wp_localize_script('gcp-app', 'gcpConfig', array('api' => esc_url_raw(rest_url('gcreation-performance/v1/')), 'nonce' => wp_create_nonce('wp_rest')));
    return '<main id="gcp-app"><h1>Website Performance Doctor</h1><p>Measure your website. Understand the evidence. Choose how to fix it.</p><form id="gcp-scan"><label>Website URL <input name="url" type="url" placeholder="https://your-website.com" required maxlength="2048"></label><button>Start free scan</button></form><p id="gcp-status" role="status" aria-live="polite"></p><ol id="gcp-events"></ol><section id="gcp-report"></section></main>';
});
add_action('admin_menu', function () {
    add_menu_page('Performance Doctor', 'Performance Doctor', 'manage_options', 'gcp', 'gcp_admin', 'dashicons-performance');
    foreach (array('Dashboard', 'Scans', 'Paid Audits', 'Expert Orders', 'Reports', 'Failed Scans', 'Settings') as $name) { add_submenu_page('gcp', $name, $name, 'manage_options', 'gcp-' . sanitize_title($name), 'gcp_admin'); }
});
function gcp_admin() {
    if (!current_user_can('manage_options')) { return; }
    if (isset($_POST['gcp_expert_update'])) {
        check_admin_referer('gcp_settings');
        $id = sanitize_text_field(wp_unslash($_POST['expert_id']));
        if (preg_match('/^[a-f0-9-]{36}$/', $id)) { gcp_engine('/admin/experts/' . $id, array('state' => sanitize_text_field(wp_unslash($_POST['expert_state'])), 'kind' => sanitize_key(wp_unslash($_POST['expert_kind']))), 'PATCH'); }
    }
    if (isset($_POST['gcp_create_product'])) {
        check_admin_referer('gcp_settings');
        if (class_exists('WC_Product_Simple') && !wc_get_product((int) get_option('gcp_product_id'))) { $product = new WC_Product_Simple(); $product->set_name('Website Performance Audit'); $product->set_virtual(true); $product->set_catalog_visibility('hidden'); $product->set_regular_price('499'); $product->set_tax_status('none'); $product->set_sold_individually(true); update_option('gcp_product_id', $product->save()); }
    }
    echo '<div class="wrap"><h1>Performance Doctor</h1><p>DEV service integration. Pricing is determined by the audit engine.</p><form method="post">'; wp_nonce_field('gcp_settings'); echo '<button class="button" name="gcp_create_product" value="1">Create audit checkout product</button></form>';
    $data = gcp_engine('/admin/summary'); if (is_wp_error($data)) { echo '<p>' . esc_html($data->get_error_message()) . '</p>'; } else { echo '<pre>' . esc_html(wp_json_encode($data, JSON_PRETTY_PRINT)) . '</pre>'; foreach (array('experts' => 'task', 'expertReviews' => 'review') as $group => $kind) { foreach ($data[$group] as $task) { echo '<form method="post">'; wp_nonce_field('gcp_settings'); echo '<p>' . esc_html($task['id'] . ' · ' . $task['state']) . '</p>'; if ($kind === 'review') { echo '<p>' . esc_html(get_option('gcp_expert_contact_' . $task['id'])) . '</p>'; } echo '<input type="hidden" name="expert_id" value="' . esc_attr($task['id']) . '"><input type="hidden" name="expert_kind" value="' . esc_attr($kind) . '"><select name="expert_state">'; foreach (array('Pending','In Review','In Progress','Waiting','Completed','Retest Required','Verified') as $state) { echo '<option>' . esc_html($state) . '</option>'; } echo '</select><button name="gcp_expert_update" value="1">Update expert state</button></form>'; } } } echo '</div>';
}

add_action('woocommerce_email_after_order_table', function ($order, $sent_to_admin, $plain_text) {
    if ($sent_to_admin || !$order->is_paid()) { return; }
    foreach ($order->get_items() as $item) {
        $token = $item->get_meta('_gcp_report_token'); if (!$token) { continue; }
        $link = home_url('/performance-doctor/') . '#report=' . rawurlencode($token);
        if ($plain_text) { echo "\nSecure Fix Center: " . esc_url_raw($link) . "\nVerify with order number and checkout email.\n"; }
        else { echo '<p><a href="' . esc_url($link) . '">Open your secure Fix Center</a>. Verify with order number and checkout email.</p>'; }
    }
}, 10, 3);
