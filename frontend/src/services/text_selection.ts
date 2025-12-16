export function getSelectedText(): string | null {
  if (typeof window === 'undefined') return null; // Ensure this runs only in browser environment
  const selection = window.getSelection();
  if (selection && selection.toString().length > 0) {
    return selection.toString();
  }
  return null;
}

export function getSelectionMetadata(): { chapter?: string; section?: string } | null {
  if (typeof window === 'undefined') return null; // Ensure this runs only in browser environment

  const selection = window.getSelection();
  if (!selection || selection.rangeCount === 0) return null;

  const range = selection.getRangeAt(0);
  let currentNode: Node | null = range.commonAncestorContainer;

  let chapter: string | undefined;
  let section: string | undefined;

  // Traverse up the DOM to find relevant Docusaurus elements (e.g., h1 for chapter, h2/h3 for section)
  while (currentNode && currentNode !== document.body) {
    if (currentNode instanceof HTMLElement) {
      if (currentNode.tagName === 'H1') {
        chapter = currentNode.textContent?.trim();
      } else if (currentNode.tagName === 'H2' || currentNode.tagName === 'H3') {
        section = currentNode.textContent?.trim();
      }
    }
    if (chapter && section) break;
    currentNode = currentNode.parentNode;
  }

  if (chapter || section) {
    return { chapter, section };
  }

  return null;
}
