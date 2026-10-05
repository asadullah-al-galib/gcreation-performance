STATUS: PENDING REVIEW — independent implementation/testing continues
PRIORITY: Required before deployed DEV acceptance
BLOCKS: DEV deployment, public proxy health, real browser resource/isolation checks, WordPress/WooCommerce E2E
WHY HUMAN ACTION IS REQUIRED: The agent has no root/Plesk authority. These actions install immutable trusted code and configure only DEV.
FILES TO REVIEW: ops/dev/install-root.sh, deploy_controller.py, deploy-dev.sh, runtime.Dockerfile, seccomp_profile.json, all systemd files, nginx-dev.conf.example, README.md; SECURITY.md
EXACT ACTION: Review the kit; install it as root; populate DENIED_IPS; apply DEV-only Plesk proxy; after deployment activate the plugin and configure DEV page/product/BDT/manual checkout. Supply a controlled public test URL with product/sitemap fixtures, owned/authorized for this project. Never grant the agent root, Docker group/socket or Plesk admin access.
EXACT COMMAND OR UI PATH: Human root: bash /home/codexperf/projects/gcreation-performance/ops/dev/install-root.sh ; Plesk DEV domain > Apache & nginx settings > Additional nginx directives ; DEV WP > Plugins > gCreation Performance Doctor ; Pages > /performance-doctor/ shortcode [gcreation_performance] ; Performance Doctor > Settings ; WooCommerce > Settings > General/Payments.
EXPECTED RESULT: Root-owned watcher and constrained runtime can accept the fixed deployment request; only the DEV plugin is replaced; public /perf-engine/health returns structured JSON; manual/test checkout is available.
VERIFICATION: .ops/deploy-dev.status COMPLETED; internal/public health; root-owned/non-writable installed files; docker inspect effective CPU/memory/PID/network flags; systemctl show gcreation-perf-dev.slice; DEV controlled E2E. Share sanitized results, never secrets.
SAFE TO CONTINUE WITHOUT THIS ACTION: Yes — engine/plugin tests, fixes, UI tests, documentation and all project-local development. No privileged kit execution by the agent.
