/**
 * College Board requires this non-affiliation notice on every page that uses
 * the SAT mark. It lives in the root layout so no page can miss it.
 */
export function SatFootnote() {
  return (
    <footer className="footnote">
      SAT<sup>®</sup> is a trademark registered by the College Board, which is not affiliated with, and does not
      endorse, this product.
    </footer>
  );
}
