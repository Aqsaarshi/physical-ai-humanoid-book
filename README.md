# Quickstart Guide: Physical AI & Humanoid Robotics Textbook Project

This guide provides a quick overview of how to set up the development environment and start contributing to the Physical AI & Humanoid Robotics Textbook project.

## 1. Prerequisites

Ensure you have the following installed on your system:

-   **Node.js**: Version 18.x or later. You can download it from [nodejs.org](https://nodejs.org/).
-   **npm** (Node Package Manager): Usually comes bundled with Node.js. Verify with `npm -v`.
-   **Git**: For version control. Download from [git-scm.com](https://git-scm.com/).

## 2. Project Setup

1.  **Clone the Repository**:
    If you haven't already, clone the project repository to your local machine:
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Install Dependencies**:
    Navigate into the project directory and install the Docusaurus dependencies:
    ```bash
    npm install
    ```

## 3. Local Development

To start the local development server and preview the textbook:

```bash
npm start
```

This will open a new browser window (usually at `http://localhost:3000`) showing the Docusaurus website. Any changes you make to the Markdown files in the `docs/` directory or configuration will trigger a live reload.

## 4. Contributing Content

-   **Chapters**: Add or edit Markdown files in the `docs/` directory (e.g., `docs/01-introduction.md`). Follow the established naming convention `docs/XX-chapter-title.md`.
-   **Assets**: Place images, diagrams, and other static assets in the `static/img/` directory. Reference them in your Markdown files like `![Alt Text](/img/your-image.png)`.
-   **Glossary/Appendix**: Update `docs/glossary.md` and `docs/appendix.md` as needed.
-   **Sidebar**: The `sidebars.js` file controls the navigation structure. Update it to include new chapters or sections.

## 5. Building for Production

To build the static website for deployment:

```bash
npm run build
```

The generated static files will be placed in the `build/` directory.

## 6. Deployment (Web)

To deploy the textbook to GitHub Pages (after configuring `docusaurus.config.js`):

```bash
npm run deploy
```

## 7. PDF Generation

Currently, PDF generation is a manual or script-driven process. After the web version is stable, follow these steps:

-   **Option 1: Docusaurus Plugin**: If a `docusaurus-plugin-pdf` or similar is integrated, follow its specific instructions.
-   **Option 2: Headless Browser Script**: A custom Node.js script using Puppeteer/Playwright will be used to print the deployed Docusaurus site to PDF. Ensure the script adheres to page count and formatting requirements. More details will be provided in the project's documentation once implemented.
