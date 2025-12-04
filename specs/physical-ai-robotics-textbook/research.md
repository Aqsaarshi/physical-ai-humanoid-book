---
description: "Research strategy for Physical AI & Humanoid Robotics Textbook implementation"
---

# Research: Physical AI & Humanoid Robotics Textbook Implementation

## Content Generation Strategy

**Decision**: Content will be authored in Markdown files within the `docs/` directory, adhering to a strict chapter structure and naming convention.  
**Rationale**: Markdown is lightweight, widely supported, and integrates seamlessly with Docusaurus. Structured approach ensures consistency and maintainability.  
**Alternatives Considered**: AsciiDoc, reStructuredText (rejected due to less direct Docusaurus integration and ecosystem support).

### Chapter Content Breakdown

- Each chapter will be a separate Markdown file (`docs/XX-chapter-title.md`).  
- Content for each chapter will include:  
  - Detailed explanations of core concepts  
  - Real-world examples to illustrate applications  
  - Relevant diagrams/visuals (referenced from `static/img/`)  
  - Mini practical tasks or conceptual exercises  
  - Short quizzes to reinforce learning  
- `docs/glossary.md` will contain definitions of technical terms.  
- `docs/appendix.md` will house supplementary information, including references.

## Local Testing & Development Workflow

**Decision**: Use Docusaurus's local dev server (`npm start`) for content preview and iteration.  
**Rationale**: Provides real-time feedback, hot-reloading, and accurate rendering before deployment.  
**Alternatives Considered**: Manual browser refresh, static HTML previews (rejected due to inefficiency).

### Quality Assurance Steps

- **Content Review**: Manual review for accuracy, clarity, grammar, and pedagogical effectiveness  
- **Link Validation**: Docusaurus checks for broken links during build (`npm run build`)  
- **Visual Integrity**: Verify all diagrams/images render correctly and are properly placed

## Git Management & Version Control

**Decision**: Continue using Git for version control with feature branches and regular descriptive commits.  
**Rationale**: Ensures traceability, collaboration, and easy rollback.  
**Alternatives Considered**: Centralized VCS (rejected; distributed preferred).

### Key Practices

- **Feature Branching**: e.g., `001-physical-ai-robotics-textbook`  
- **Commit Hygiene**: Small, atomic commits with clear messages  
- **Regular Pushing**: Frequent pushes to remote repository for backup and collaboration

## GitHub Pages Deployment

**Decision**: Use Docusaurus deployment to GitHub Pages for hosting the web version.  
**Rationale**: Free, simple, effective, and integrates directly with GitHub.  
**Alternatives Considered**: Netlify, Vercel, AWS S3 (rejected for simplicity)

### Deployment Process

- **Configuration**: Update `docusaurus.config.js` with `baseUrl`, `projectName`, `organizationName`  
- **Build & Deploy**: Run `docusaurus deploy` (or `npm run deploy`) to build and push to `gh-pages` branch  
- **PDF Generation**: After site is stable, generate PDF (`FR-008`) by:  
  - Investigating `docusaurus-plugin-pdf` for integration  
  - If unsuitable, create custom Node.js script using Puppeteer/Playwright to programmatically print site to PDF  
  - Ensure page count 80–120 (`FR-006`)
