export type JobState =
  | "PENDING"
  | "RUNNING"
  | "COMPLETED"
  | "FAILED"
  | "WAITING_FOR_RESOURCES"
  | "RETRYING";
export type Scope = "free" | "major5" | "full" | "retest";
export type Mode = "self" | "expert";
export interface Resource {
  url: string;
  type: string;
  status: number | null;
  bytes: number | null;
  durationMs: number | null;
  cacheControl?: string;
  encoding?: string;
  mime?: string;
  renderBlocking?: boolean;
}
export interface Metrics {
  url: string;
  status: number | null;
  redirects: number;
  ttfbMs: number | null;
  loadMs: number | null;
  requests: number;
  transferredBytes: number | null;
  jsBytes: number | null;
  cssBytes: number | null;
  imageBytes: number | null;
  fontBytes: number | null;
  thirdPartyRequests: number;
  failedRequests: number;
  resources: Resource[];
  lighthouse: Partial<
    Record<
      "lcpMs" | "cls" | "fcpMs" | "tbtMs" | "speedIndexMs" | "performanceScore",
      number
    >
  >;
}
export interface Issue {
  rule_id: string;
  category: string;
  severity: "critical" | "important" | "opportunity";
  title: string;
  affected_url: string;
  evidence: string[];
  measured_values: Record<string, number | string>;
  threshold: number | string;
  impact: string;
  recommendation: string;
  steps: string[];
  verification_method: string;
}
export interface Inventory {
  urls: { url: string; kind: string }[];
  count: number;
  truncated: boolean;
  sitemaps: string[];
  wordpress: boolean;
  woocommerce: boolean;
}
export interface Audit {
  id: string;
  url: string;
  scope: Scope;
  state: JobState;
  parent_id: string | null;
  inventory: Inventory | null;
  report: Report | null;
  error: string | null;
}
export interface Report {
  healthScore: number | null;
  scoreBasis: string;
  pages: Metrics[];
  issues: Issue[];
  incomplete: string[];
  createdAt: string;
}
export type Emit = (type: string, data?: Record<string, unknown>) => void;
