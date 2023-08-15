<a id="readme-top"></a> 



<!-- PROJECT SUMMARY -->
<br />
<div align="center">
  <img src="https://i.imgur.com/g08ozNS.png" alt="Logo" width="400px">
  <br />
  <p align="center">
    Automatically generate documentation for Python projects
    <br />
    <a href="https://scandocs-documentation.vercel.app/"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="#about-the-project">Getting Started</a>
    ·
    <a href="#basic-usage">Usage</a>
    ·
    <a href="https://github.com/Kieran-Lock/ScanDocs/blob/main/LICENSE">License</a>
  </p>
</div>



<!-- ABOUT THE PROJECT -->
## About the Project

ScanDocs creates documentation for Python projects automatically, by harnessing the power of SvelteKit, and Python's dynamic nature. By using signature analysis of your modules, classes, and subroutines, and a little help from your docstrings, ScanDocs is able to generate comprehensive and flexible documentation, with customizable themes, easily adaptable content, and comprehensive searching functionality.  
  
If you're familiar with SvelteKit, you can then adjust the website layout however you think best fits your project, and edit website content easily from the generated JSON tree. Themes can also be easily changed by using Skeleton UI's [theme generator](https://www.skeleton.dev/docs/generator).




<!-- GETTING STARTED -->
## Getting Started

ScanDocs is available on PyPI. To use it in your project, run:

```
pip install ScanDocs
```

To install specific previous versions, take a look at the version history, locate the version tag (vX.Y.Z), and run:

```
pip install ScanDocs==X.Y.Z
```



<!-- BASIC USAGE EXAMPLES -->
## Basic Usage

### Initial Documentation

ScanDocs requires very little configuration. Without any fancy tricks and adjustments, you can generate perfectly suitable documentation!  
To start generating documentation, first import the correct modules:
```py
from scandocs import Package, Documentation
from pathlib import Path
import <your_project>  # The one you want to document
```

Tell ScanDocs what to call your project, and where it should be saved:
```py
WEBSITE_PATH = Path("./docs")  # Or wherever you want your website files to be saved
PROJECT_NAME = "YOUR_PROJECT_NAME"  # The name of your project
```

Then, scan your project, so ScanDocs knows what you've built:
```py
project = Package.from_module(<your_project>)
```

Next, configure the documentation:
```py
docs = Documentation(project, WEBSITE_PATH, Configuration(PROJECT_NAME))  # Set the path to be wherever you want the website files to be saved
```

You can now build the website files:
```py
docs.output()
```

In your targetted directory, run the following command to see your website in developer mode:
```
npm run dev
```

You now have a full website built with SvelteKit and Skeleton UI. Look at the documentation of these tools to see what to do next!
* [SvelteKit](https://kit.svelte.dev/docs/introduction)
* [SkeletonUI](https://www.skeleton.dev/docs)

You can configure your website further, by importing `Themes`:
```py
from scandocs import Package, Documentation, Configuration, Themes
from pathlib import Path
import <your_project>  # The one you want to document


WEBSITE_PATH = Path("./docs")  # Or wherever you want your website files to be saved
PROJECT_NAME = "YOUR_PROJECT_NAME"  # The name of your project


project = Package.from_module(<your_project>)
docs = Documentation(project, WEBSITE_PATH, Configuration(PROJECT_NAME, theme=Themes.GOLD_NOUVEAU))  # Or any other available theme you want
docs.output()
```
You can now generate comprehensive documentation, with any theme you want, for all of your Python projects!



<!-- LICENSE -->
## License

Distributed under the GNU General Public License v3.0 License. See [LICENSE](https://github.com/Kieran-Lock/ScanDocs/blob/main/LICENSE) for further details.

<p align="right">(<a href="#readme-top">Back to Top</a>)</p>
