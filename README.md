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
  <a href="https://github.com/blaine-t/fwd_outlook_graph">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">fwd_outlook_graph</h3>

  <p align="center">
    AKA FOG 
    <br />
    <a href="https://github.com/blaine-t/fwd_outlook_graph/docs"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/blaine-t/fwd_outlook_graph/issues">Report Bug</a>
    ·
    <a href="https://github.com/blaine-t/fwd_outlook_graph/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project is a hobby project of mine to use the Microsoft Graph API to forward emails from an Outlook account to any number of other email accounts automatically when you receive an email.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][Python]][Python-url]
* [![Flask][Flask]][Flask-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

* [Python 3](https://www.python.org/downloads/)

### Installation

1. Setup an [Azure App](docs/azure_setup.md)
2. Clone the repo
   ```sh
   git clone https://github.com/blaine-t/fwd_outlook_graph.git
   cd fwd_outlook_graph
   ```
3. Setup venv
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   python3 -m pip install -r requirements.txt
   ```
4. Configure [config.py](fwd_outlook_graph/config.example.py) to your needs
    ```sh
    cd fwd_outlook_graph
    cp config.example.py config.py
    nano config.py
    ```
6. Run the app
  * Development
    ```sh
    python3 main.py
    ```
  * Production
    ```sh
    gunicorn main:app -b 127.0.0.1:5000
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Forward emails automatically with extra features like:

* Catch-all email addresses
* Custom subjects
* Multiple forwarding addresses

_For more examples, please refer to the [Documentation](docs/usage)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [X] Get access token from Graph (Microsoft Graph API)
- [X] Forward messages with Graph
- [X] Read messages from Graph
- [X] Send messages with Graph
- [X] Cache access token
- [X] Increase security with clientState
- [X] Add subscriptions
    - [X] lifeCycle support
- [X] Development tool routes
- [X] Development tool page
- [X] Move to pure python config
- [X] Encrypt cache when possible
- [ ] Write documentation
- [ ] Improve error handling

See the [open issues](https://github.com/blaine-t/fwd_outlook_graph/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the GPL-3.0 License. See [`LICENSE`](LICENSE) for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Blaine Traudt - [blaine-t](https://github.com/blaine-t) - blaine-t@bathost.net

Project Link: [https://github.com/blaine-t/fwd_outlook_graph](https://github.com/blaine-t/fwd_outlook_graph)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Microsoft Graph Documentation](https://learn.microsoft.com/en-us/graph/)
* [Flask Documentation](https://flask.palletsprojects.com/en/2.3.x/)
* [darrenjrobinson's example](https://gist.github.com/darrenjrobinson/553ea10e304246ebfa1eac6dde0cf63b/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/blaine-t/fwd_outlook_graph.svg?style=for-the-badge
[contributors-url]: https://github.com/blaine-t/fwd_outlook_graph/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/blaine-t/fwd_outlook_graph.svg?style=for-the-badge
[forks-url]: https://github.com/blaine-t/fwd_outlook_graph/network/members
[stars-shield]: https://img.shields.io/github/stars/blaine-t/fwd_outlook_graph.svg?style=for-the-badge
[stars-url]: https://github.com/blaine-t/fwd_outlook_graph/stargazers
[issues-shield]: https://img.shields.io/github/issues/blaine-t/fwd_outlook_graph.svg?style=for-the-badge
[issues-url]: https://github.com/blaine-t/fwd_outlook_graph/issues
[license-shield]: https://img.shields.io/github/license/blaine-t/fwd_outlook_graph.svg?style=for-the-badge
[license-url]: https://github.com/blaine-t/fwd_outlook_graph/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/blaine-traudt-832381221
[Python]: https://img.shields.io/badge/python-ffd343?style=for-the-badge&logo=python
[Python-url]: https://www.python.org/
[Flask]: https://img.shields.io/badge/flask-60bbc9?style=for-the-badge&logo=flask&logoColor=ffffff
[Flask-url]: https://flask.palletsprojects.com/en/2.3.x/