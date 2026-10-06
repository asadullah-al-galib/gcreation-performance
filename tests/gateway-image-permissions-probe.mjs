// Read-only probe. Run the CLI only in the separately approved fresh image,
// as UID:GID10001:10001, with no network, secrets, or official runtime mounts.
import assert from "node:assert/strict";
import { constants } from "node:fs";
import { access, lstat, readFile } from "node:fs/promises";
import { createHash } from "node:crypto";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";

const gatewaySha256 =
  "d9616a205b5f7a7e2d11779a2a98a1a5367ec76d992b2d3b8bb51e5a25343c4c";

export async function verifyGatewayImage(fixture) {
  // Ordinary-user regression fixtures explicitly identify their limited scope.
  // The CLI never accepts fixture overrides or a caller-supplied expected hash.
  const root = fixture ? resolve(fixture.root) : "/opt/gcreation-trusted";
  const owner = fixture ? process.getuid() : 0;
  const group = fixture ? process.getgid() : 0;
  if (!fixture) {
    assert.equal(process.getuid(), 10001);
    assert.equal(process.getgid(), 10001);
  }
  const directories = fixture
    ? [root]
    : ["/", "/opt", "/opt/gcreation-trusted"];
  directories.push(`${root}/ops`, `${root}/ops/dev`, `${root}/ops/dev/trusted`);
  const observations = [];
  for (const path of directories) {
    const info = await lstat(path);
    assert.ok(info.isDirectory(), path);
    assert.equal(info.uid, owner, path);
    assert.equal(info.gid, group, path);
    assert.equal(info.mode & 0o7777, 0o755, path);
    assert.equal(info.mode & 0o022, 0, path);
    await access(path, constants.X_OK);
    observations.push({ path, uid: info.uid, gid: info.gid, mode: "0755" });
  }
  const gateway = `${root}/ops/dev/trusted/gateway.mjs`;
  const info = await lstat(gateway);
  assert.ok(info.isFile(), gateway);
  assert.equal(info.nlink, 1, gateway);
  assert.equal(info.uid, owner, gateway);
  assert.equal(info.gid, group, gateway);
  assert.equal(info.mode & 0o7777, 0o644, gateway);
  await access(gateway, constants.R_OK);
  const actualHash = createHash("sha256")
    .update(await readFile(gateway))
    .digest("hex");
  assert.equal(actualHash, gatewaySha256);
  // Dynamic import does not enter the gateway's main/listen branch.
  const module = await import(pathToFileURL(gateway).href);
  assert.equal(typeof module.createGateway, "function");
  observations.push({
    path: gateway,
    uid: info.uid,
    gid: info.gid,
    mode: "0644",
    sha256: actualHash,
  });
  return {
    scope: fixture ? "ORDINARY_USER_FIXTURE" : "FRESH_IMAGE_UID10001",
    uid: process.getuid(),
    gid: process.getgid(),
    observations,
    traversal: "PASS",
    read: "PASS",
    dynamicImport: "PASS",
  };
}

if (
  process.argv[1] &&
  import.meta.url === pathToFileURL(process.argv[1]).href
) {
  assert.equal(process.argv.length, 2, "No CLI permission overrides allowed");
  console.log(JSON.stringify(await verifyGatewayImage()));
}
