import { createHash, randomBytes, timingSafeEqual } from "node:crypto";
export const newToken = () => randomBytes(32).toString("base64url");
export const hashToken = (token: string) =>
  createHash("sha256").update(token).digest("hex");
export function secretMatches(value: string, expected: string) {
  if (!expected || value.length > 512) return false;
  return timingSafeEqual(
    createHash("sha256").update(value).digest(),
    createHash("sha256").update(expected).digest(),
  );
}
export function reportAuthorized(
  token: string,
  storedHash: string,
  suppliedOrder: string,
  storedOrder: string,
  contact: string,
  contactHash: string,
) {
  return (
    token.length >= 32 &&
    secretMatches(hashToken(token), storedHash) &&
    secretMatches(suppliedOrder, storedOrder) &&
    secretMatches(hashToken(contact.trim().toLowerCase()), contactHash)
  );
}
