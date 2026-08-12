# Build and Outputs

The build boundary converts the content directory into isolated language sites and strict PDFs, then removes synchronized intermediates so source does not become a second uncontrolled content source.

| Goal | Command | When |
| --- | --- | --- |
| Check the environment | python build_local.py --check | After configuration changes or before CI |
| Fast web validation | python build_local.py --clean --no-pdf | Daily authoring |
| Browse locally | python build_local.py --clean --no-pdf --serve | Check links, navigation, and visuals |
| Delivery validation | python build_local.py --clean | Before merge, tag, or release |

See [Local Build Workflow](01_local_build.md) and [PDF Delivery](02_pdf_delivery.md). Web and PDF share one DocumentCatalog; content or asset issues should surface locally before CI repeats the check.
