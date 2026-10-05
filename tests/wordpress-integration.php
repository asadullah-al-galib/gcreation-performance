<?php
// Unprivileged WooCommerce contract harness. Does not load or modify DEV WordPress.
define('ABSPATH', __DIR__);
define('GCREATION_ENGINE_SECRET', str_repeat('x', 64));
define('HOUR_IN_SECONDS', 3600); define('DAY_IN_SECONDS', 86400);
$options = array(); $hooks = array(); $transients = array(); $requests = array(); $order = null;
class WP_Error { public $message; public function __construct($code, $message, $data = null) { $this->message = $message; } }
function add_action($name, $fn, $priority = 10, $args = 1) { global $hooks; $hooks[$name][] = $fn; }
function add_shortcode($name, $fn) {}
function is_wp_error($value) { return $value instanceof WP_Error; }
function wp_json_encode($data) { return json_encode($data); }
function wp_remote_request($url, $args) {
    global $requests; $data = json_decode($args['body'], true); $requests[] = array($url, $data);
    if (strpos($url, '/quotes') !== false) { return array('code' => 200, 'body' => json_encode(array('amount'=>499,'currency'=>'BDT','count'=>5,'tier'=>'major5','websiteUrl'=>'https://example.com/'))); }
    if (strpos($url, '/orders/paid') !== false) { return array('code'=>201, 'body'=>json_encode(array('auditId'=>'paid-audit-id'))); }
    return array('code'=>503,'body'=>'{}');
}
function wp_remote_retrieve_response_code($response) { return $response['code']; }
function wp_remote_retrieve_body($response) { return $response['body']; }
function get_transient($key) { global $transients; return isset($transients[$key]) ? $transients[$key] : false; }
function set_transient($key, $value, $duration) { global $transients; $transients[$key]=$value; }
function sanitize_text_field($value) { return $value; }
function sanitize_key($value) { return $value; }
function get_woocommerce_currency() { return 'BDT'; }
function add_option($key,$value,$deprecated='',$autoload=false) {global $options;if(isset($options[$key]))return false;$options[$key]=$value;return true;}
function get_option($key) {global $options;return isset($options[$key])?$options[$key]:123;}
function wc_get_product($id) { return $id===123 ? new stdClass() : false; }
function wc_get_checkout_url() { return 'https://dev.gcreation.agency/checkout/'; }
function wc_get_order($id) { global $order; return $order; }
function wp_next_scheduled($hook, $args) { return false; }
function wp_schedule_single_event($time,$hook,$args) {}
class Cart { public $added; public function add_to_cart($id,$quantity,$variation,$attrs,$data) { $this->added=$data; return 'cart-key'; } }
$wc = new stdClass(); $wc->cart = new Cart();
function WC() { global $wc; return $wc; }
class Item { public $meta=array(); public function get_meta($key) { return isset($this->meta[$key])?$this->meta[$key]:null; } public function update_meta_data($key,$value) { $this->meta[$key]=$value; } public function save() {} public function get_total() { return 499; } }
class Order { public $meta=array(); public $item; public function __construct($item) {$this->item=$item;} public function is_paid() {return true;} public function get_items() {return array($this->item);} public function get_billing_email() {return 'buyer@example.com';} public function get_currency() {return 'BDT';} public function add_order_note($note) {} public function get_meta($key) {return isset($this->meta[$key])?$this->meta[$key]:null;} public function update_meta_data($key,$value) {$this->meta[$key]=$value;} public function save() {} }
class Request { private $data; public function __construct($data) {$this->data=$data;} public function get_param($name) {return isset($this->data[$name])?$this->data[$name]:null;} }
function check($condition,$message) {if(!$condition){fwrite(STDERR,$message."\n");exit(1);}}
require __DIR__ . '/../wordpress/gcreation-performance/gcreation-performance.php';
$_COOKIE['gcp_session']=str_repeat('a',64);
$id='11111111-1111-4111-8111-111111111111';set_transient('gcp_scan_'.$id,gcp_session(),86400);
$result=gcp_checkout(new Request(array('auditId'=>$id,'scope'=>'major5','mode'=>'self','amount'=>1)));
check(!is_wp_error($result),'Checkout rejected valid session');check(WC()->cart->added['gcp']['quote']['amount']===499,'Browser price was trusted');
$foreign=gcp_checkout(new Request(array('auditId'=>'22222222-2222-4222-8222-222222222222','scope'=>'major5','mode'=>'self')));check(is_wp_error($foreign),'Foreign scan was accessible');
$item=new Item();$item->meta['_gcp_selection']=WC()->cart->added['gcp'];$order=new Order($item);
gcp_paid_order(42);gcp_paid_order(42);
$paid=array_filter($requests,function($request){return strpos($request[0],'/orders/paid')!==false;});
check(count($paid)===1,'Payment hook duplicated paid audit');check(strlen($item->meta['_gcp_report_token'])===64,'Token is not strong');check($item->meta['_gcp_paid_audit']==='paid-audit-id','Paid audit metadata missing');
echo "WooCommerce contract: trusted pricing, session ownership and idempotent synchronization passed.\n";
