import React, { useEffect } from 'react';

interface TextSelectionProps {
  onTextSelected: (selectedText: string) => void;
}

const TextSelection: React.FC<TextSelectionProps> = ({ onTextSelected }) => {
  useEffect(() => {
    const handleSelection = () => {
      const selectedText = window.getSelection()?.toString().trim();
      if (selectedText) {
        onTextSelected(selectedText);
      }
    };

    document.addEventListener('mouseup', handleSelection);

    return () => {
      document.removeEventListener('mouseup', handleSelection);
    };
  }, [onTextSelected]);

  return null; // This component doesn't render anything, it just handles text selection
};

export default TextSelection;