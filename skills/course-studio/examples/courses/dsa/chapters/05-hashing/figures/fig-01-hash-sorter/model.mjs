// Truth for fig-01-hash-sorter: separate chaining in a table of 8 buckets, slot = k % 8.
// The chapter's text uses exactly these key sets and numbers.
export const M = 8;
export const SETS = [
  [10, 22, 31, 4, 15], // typical keys: longest chain 2 at load 5/8
  [8, 16, 24, 32, 40], // multiples of 8: every key lands in slot 0, chain 5 at load 5/8
];
export const slotOf = (key) => key % M;

// The 12 states the figure steps through: set A empty, A after 1..5 inserts, set B empty, B after 1..5.
export const STATES = SETS.flatMap((keys, set) => keys.map((_, i) => i).concat(keys.length).sort((a, b) => a - b).map((n) => ({ set, n })));

export function tableAt({ set, n }) {
  const chains = Array.from({ length: M }, () => []);
  SETS[set].slice(0, n).forEach((key) => chains[slotOf(key)].push(key));
  return chains;
}

export function readoutAt({ set, n }) {
  if (n === 0) return `empty · α 0/${M}`;
  const key = SETS[set][n - 1];
  const slot = slotOf(key);
  const chain = tableAt({ set, n })[slot].length;
  return `key ${key} → slot ${slot} · chain ${chain} · α ${n}/${M}`;
}
