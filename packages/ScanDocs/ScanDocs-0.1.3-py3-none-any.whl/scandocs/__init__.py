"""
A tool to automatically generate documentation for Python projects.

ScanDocs allows for users to document their Python projects autonomously,
utilizing the power of SvelteKit to create both beautiful and adaptable documentation
websites for Python packages of any size and complexity.
"""


from .structures import Package, Structure, SourceStructure, SignatureStructure, SearchableStructure
from .documentation import Documentation, Configuration, Themes
from .tags import ContextManager, Deprecated, Private, Example, Link, Note, Tag


Example(
    "Basic Usage",
    """from scandocs import Package, Documentation, Configuration
from pathlib import Path
import <your_project>  # The one you want to document


WEBSITE_PATH = Path("./docs")  # Or wherever you want your website files to be saved
PROJECT_NAME = "YOUR_PROJECT_NAME"  # The name of your project


project = Package.from_module(<your_project>)
docs = Documentation(project, WEBSITE_PATH, Configuration(PROJECT_NAME))  # Set the path to be wherever you want the website files to be saved
docs.output()""",
    "You can generate high-quality, comprehensive documentation with just these 8 lines of code."
).tag(Example.module_from_name(__name__))
Example(
    "Using Themes",
    """from scandocs import Package, Documentation, Configuration, Themes
from pathlib import Path
import <your_project>  # The one you want to document


WEBSITE_PATH = Path("./docs")  # Or wherever you want your website files to be saved
PROJECT_NAME = "YOUR_PROJECT_NAME"  # The name of your project


project = Package.from_module(<your_project>)
docs = Documentation(project, WEBSITE_PATH, Configuration(PROJECT_NAME, theme=Themes.GOLD_NOUVEAU))  # Or any other available theme you want
docs.output()""",
    "This code would now use the gold-nouveau theme, instead of the default theme."
).tag(Example.module_from_name(__name__))
Link(
    "PyPI",
    "https://pypi.org/project/ScanDocs/",
    "The PyPI page for ScanDocs, including instructions regarding installation."
).tag(Example.module_from_name(__name__))
Link(
    "GitHub",
    "https://github.com/Kieran-Lock/ScanDocs",
    "More information about ScanDocs, including the source code."
).tag(Example.module_from_name(__name__))
Link(
    "SkeletonUI",
    "https://www.skeleton.dev/docs/introduction",
    "ScanDocs uses SkeletonUI to build aesthetic documentation and manage themes."
).tag(Example.module_from_name(__name__))
Link(
    "SvelteKit",
    "https://kit.svelte.dev/docs/introduction",
    "ScanDocs builds websites with SvelteKit - see what you can do after generation with the SvelteKit documentation."
).tag(Example.module_from_name(__name__))
