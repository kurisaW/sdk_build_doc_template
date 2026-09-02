# Build and Outputs

The build boundary converts the content directory into isolated language sites and strict PDFs, then removes synchronized intermediates so source does not become a second uncontrolled content source.

| Goal | Command | When |
| --- | --- | --- |
| Check the environment | python build_local.py --check | After configuration changes or before CI |
| Fast web validation | python build_local.py --clean --no-pdf | Daily authoring |
| Browse locally | python build_local.py --clean --no-pdf --serve | Check links, navigation, and visuals |
| Delivery validation | python build_local.py --clean | Before merge, tag, or release |

See [Local Build Workflow](01_local_build.md) and [PDF Delivery](02_pdf_delivery.md). Web and PDF share one DocumentCatalog; content or asset issues should surface locally before CI repeats the check.

## Web Layout and Responsive Behavior

The site uses a left global tree, a center article, and a right local outline. The reading column changes continuously between 680px and 960px, while the outline stays roughly 220px to 280px. A container query evaluates the actual .wy-nav-content width and stacks the columns only when the article, outline, and gap cannot fit together. On narrow screens the outline moves below the article, avoiding horizontal scrolling and artificial left or right whitespace.

The outline reads only the current article h2/h3 headings, emits plain-text labels, and preserves nested levels. Clicks scroll smoothly and IntersectionObserver updates the active item. navigation_state.js stores the expanded path so document and in-page navigation do not collapse the user context.
