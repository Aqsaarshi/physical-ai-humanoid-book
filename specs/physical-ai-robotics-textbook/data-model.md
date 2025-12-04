# Data Model: Physical AI & Humanoid Robotics Textbook

## Entities

### Chapter
-   **Description**: Represents a distinct section of the textbook.
-   **Fields**:
    -   `id`: Unique identifier (e.g., "01", "02", ..., "10").
    -   `title`: The title of the chapter (e.g., "Introduction to Physical AI & Robotics").
    -   `short_description`: A brief summary of the chapter's content.
    -   `markdown_file_path`: Relative path to the Markdown file containing the chapter content (e.g., `docs/01-introduction.md`).
    -   `diagrams_list`: A list of associated Diagram/Visual entities.
    -   `content`: The full textual and structural content of the chapter, written in Markdown.
-   **Relationships**: Has a one-to-many relationship with `Diagram/Visual` (a chapter can have multiple diagrams).

### Glossary Term
-   **Description**: A technical term or phrase used in the textbook.
-   **Fields**:
    -   `term`: The technical word or phrase (e.g., "Kinematics").
    -   `definition`: The clear and concise explanation of the term.
-   **Relationships**: None directly with other entities, but terms are referenced throughout `Chapter` content.

### Diagram/Visual
-   **Description**: An image, illustration, or graph that visually explains a concept.
-   **Fields**:
    -   `id`: Unique identifier for the visual.
    -   `file_path`: Relative path to the image file (e.g., `static/img/robot-arm-kinematics.png`).
    -   `description`: A textual explanation of what the diagram depicts and its purpose.
    -   `alt_text`: Alternative text for accessibility.
-   **Relationships**: Belongs to a `Chapter`.

### Reference
-   **Description**: A citation for external source material.
-   **Fields**:
    -   `id`: Unique identifier for the reference.
    -   `citation`: The full citation string, formatted in either APA or IEEE style.
    -   `type`: (e.g., "book", "journal article", "website").
    -   `author(s)`: The author(s) of the source.
    -   `year`: Publication year.
    -   `title`: Title of the work.
    -   `publisher`/`journal`/`URL`: Relevant publication details.
-   **Relationships**: Referenced from `Chapter` content and listed in the Appendix.
