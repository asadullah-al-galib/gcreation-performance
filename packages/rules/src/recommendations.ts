export interface ExplanationProvider {
  steps(ruleId: string): string[];
}
// This adapter operates only on deterministic rule IDs. It cannot invent or
// replace measurements. A future explanation provider must preserve evidence.
export class TemplateExplanationProvider implements ExplanationProvider {
  steps(ruleId: string) {
    const fixes: Record<string, string[]> = {
      slow_ttfb: [
        "Retest the affected public page while logged out to establish its current server-response baseline.",
        "Inspect existing page-cache headers and hosting cache settings. If WordPress is detected, review the existing cache configuration on staging.",
        "Enable appropriate public-page caching or ask your host to investigate slow application/database work. Exclude checkout, account and private report pages.",
      ],
      poor_lcp: [
        "Record a fresh page load in the browser Performance panel and inspect the largest-contentful-paint element.",
        "If the element is an image, size and compress it for its rendered dimensions. Ensure the visible hero image is not deferred by unnecessary lazy loading.",
        "Reduce the measured work before that element renders, changing one resource at a time.",
      ],
      high_blocking: [
        "Record a page load in the Performance panel and inspect long main-thread tasks.",
        "Identify the script URLs and features associated with those tasks; do not assume a plugin cause from the score alone.",
        "Remove unused code or delay optional features until interaction. Test forms and checkout after each staging change.",
      ],
      excessive_requests: [
        "Open the Network panel on a fresh load and group requests by type and initiator.",
        "List which visible features need each optional group of requests.",
        "Remove or delay unused groups one at a time, retaining essential forms and commerce behavior.",
      ],
      page_weight: [
        "Open the Network panel and sort resources by transferred size.",
        "Start with the largest observed images, scripts and fonts; preserve the originals in your backup.",
        "Replace one oversized resource at a time with a smaller version and verify appearance on mobile and desktop.",
      ],
      javascript_payload: [
        "Filter the Network panel to JavaScript and inspect the largest files.",
        "Use the Coverage panel to locate unused code, then identify the corresponding feature or theme asset.",
        "Remove unused features or split/defer optional code on staging. Retest menus, forms and checkout.",
      ],
      css_payload: [
        "Filter the Network panel to stylesheets and compare their transferred sizes.",
        "Use Coverage to inspect unused styles for the affected page.",
        "Remove unused styles through the theme/build configuration on staging, preserving responsive and interactive states.",
      ],
      third_party: [
        "Group Network requests by domain and identify the purpose of each third-party service.",
        "Separate essential payment/security functionality from optional analytics, chat and widgets.",
        "Delay or remove optional services and verify consent behavior and essential checkout features.",
      ],
      font_overhead: [
        "List loaded font files and the families/weights actually used on this page.",
        "Remove unused font weights and families through the theme or style configuration.",
        "Subset only when required languages and glyphs are preserved, then verify text appearance and loading behavior.",
      ],
      redirect_chain: [
        "Follow the affected navigation URL in the Network panel and record each redirect.",
        "Update internal navigation, sitemap and canonical references to the final intended HTTPS URL.",
        "Retest the original and updated links; keep redirects needed for security and old bookmarked URLs.",
      ],
      oversized_images: [
        "Open the listed image URLs and check their rendered dimensions in the page.",
        "Create compressed variants close to the rendered dimensions while preserving the original files.",
        "Update the page/media references and responsive image variants; verify image quality on mobile and desktop.",
      ],
      modern_images: [
        "Create WebP or AVIF variants of the listed JPEG/PNG images.",
        "Compare file size and visible quality before replacing an asset.",
        "Serve compatible variants with a suitable fallback and check that every image request succeeds.",
      ],
      render_blocking: [
        "Inspect the resources identified as blocking in a fresh browser performance recording.",
        "Keep styles required for the initial visible layout; move optional scripts or styles later through the theme/build configuration.",
        "Test rendering and interactions after each change, then compare the observed loading metrics.",
      ],
      failed_resources: [
        "Open each listed failed URL and inspect its current HTTP status and requesting page.",
        "Correct missing asset references or investigate the corresponding access/server error with the site owner.",
        "Reload with the Network panel open and confirm the resource now returns successfully.",
      ],
      cache_policy: [
        "Inspect Cache-Control for the listed public static resources.",
        "Configure a suitable cache lifetime in the host/CDN for versioned images, scripts and fonts.",
        "Keep private pages, checkout, account and report responses excluded. Change resource versions when content changes.",
      ],
      compression: [
        "Inspect Content-Encoding and transferred size for the listed text resources.",
        "Ask your hosting provider or configure the existing site-level server/CDN to enable supported text compression.",
        "Reload without browser cache and confirm compression is actually observed, then compare transferred bytes.",
      ],
    };
    return [
      "Back up the site and use staging before changing live behavior.",
      ...(fixes[ruleId] ?? ["Review the observed evidence with an expert."]),
      "Run a fresh targeted retest. A fixed checkbox is only your claim; compare the new measurements before declaring success.",
    ];
  }
}
export const explanations: ExplanationProvider =
  new TemplateExplanationProvider();
