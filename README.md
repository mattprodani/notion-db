<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/mattprodani/notion-db">
    <img src="https://github.com/mattprodani/notion-db/raw/6e881060ffebffbb24fcb6f41262907f3f72219e/assets/notion_logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Notion-DB</h3>

  <p align="center">
    Notion-DB is a powerful object-oriented client for the Notion API that allows you to easily access and work with notion Databases. Learn how to use it and create your own Notion integrations in minutes!
    <br />
    <a href="https://notion-db.rtfd.io"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <!-- <a href="https://github.com/mattprodani/notion-db">View Demo</a> -->
    <!-- · -->
    <a href="https://github.com/mattprodani/notion-db/issues">Report Bug</a>
    ·
    <a href="https://github.com/mattprodani/notion-db/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->
Notion-DB is a powerful object-oriented client for the Notion API that allows you to easily access and work with notion Databases. Learn how to use it and create your own Notion integrations in minutes!

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

This is an example on how to get started with using the API client. To see more specific uses
please refer to the [Documentation](https://notion-db.rtfd.io). Also refer to the Notion API documentation for more information on the API itself.

### Installation

1. Install the package using pip

   ```sh
   pip install notion-toolkit
   ```

2. Get an API key at [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)

### Example Usage

#### Adding a row to an existing database

<img src = "https://raw.githubusercontent.com/mattprodani/notion-db/master/assets/example_code.svg" height = 300>

#### Update Notion database properties with custom Schema objects

<img src = "https://raw.githubusercontent.com/mattprodani/notion-db/master/assets/custom_db.svg" height = 450>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Package Overview

### The main classes are: **Connector, Database, Row, and Schema**

- **Connector** objects are used to connect to the Notion API and work with the API.

- **Schema** objects are used to create new databases and rows. They are also used to update existing databases and rows. Schema objects only contain the structure of the database or row, not the data.

- **Row**  objects contain values, and work with existing rows and create new ones. They are similar to Pandas series,

- **Database** objects are used to work with existing databases and create new ones, as a collection of rows.

### Schema and Row objects contain Properties

**Property Values** make up each entry in a Row object, and they contain values and properties for a row cell. The client supports all property types that are supported by the Notion API and makes it easy to automatically parse Python types.

**Schema Properties** are used to create new databases and rows, or to validate row objects. They do not hold any values, but hold attributes about the column type in the database, such as the name, and format. The client supports all property types that are supported by the Notion API.

_For more examples, please refer to the [Documentation](https://notion-db.rtfd.io)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Please feel free to contribute in any way!

<!-- LICENSE -->
## License

Distributed under the GNU 3 License.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Matt Prodani - mattp@nyu.edu

Repository Link: [https://github.com/mattprodani/notion-db](https://github.com/mattprodani/notion-db)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/mattprodani/notion-db.svg?style=for-the-badge
[contributors-url]: https://github.com/mattprodani/notion-db/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/mattprodani/notion-db.svg?style=for-the-badge
[forks-url]: https://github.com/mattprodani/notion-db/network/members
[stars-shield]: https://img.shields.io/github/stars/mattprodani/notion-db.svg?style=for-the-badge
[stars-url]: https://github.com/mattprodani/notion-db/stargazers
[issues-shield]: https://img.shields.io/github/issues/mattprodani/notion-db.svg?style=for-the-badge
[issues-url]: https://github.com/mattprodani/notion-db/issues
[license-shield]: https://img.shields.io/github/license/mattprodani/notion-db.svg?style=for-the-badge
[license-url]: https://github.com/mattprodani/notion-db/blob/master/src/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/mattprodani
