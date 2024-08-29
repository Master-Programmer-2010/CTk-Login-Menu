<h1 align="center">
  <a href="https://amplication.com/#gh-light-mode-only">
  <img src="images/CTk_Login_Menu_Banner_Light.png">
  </a>
  <a href="https://amplication.com/#gh-dark-mode-only">
  <img src="images/CTk_Login_Menu_Banner_Dark.png">
  </a>
</h1>

<h4 align="center">A login system built with <a href="https://github.com/TomSchimansky/CustomTkinter" target="_blank">CustomTkinter</a>.</h4>

<p align="center">
  <img src="https://img.shields.io/github/downloads/Master-Programmer-2010/CTk-Login-Menu/total?label=Downloads" alt="Downloads Badge">
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt=License: MIT>
  </a>
  <img src="https://img.shields.io/github/v/release/Master-Programmer-2010/CTk-Login-Menu?label=Release" alt=Github release (latest by date)>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.9%2B-blue.svg" alt="Python Badge">
  </a>
</p>

<p align="center">
  <a href="#screenshots">Screenshots</a> • 
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#download">Download</a> •
  <a href="#license">License</a>
</p>

## Screenshots

<p align="center">
  <img src="images/login_menu_screenshot.png" alt="Login Menu Image" width="45%" />
  <img src="images/sign_up_menu_screenshot.png" alt="Sign Up Menu Image" width="45%" />

<p align="center">
  <img src="images/admin_menu_screenshot.png" alt="Admin Menu" width="45%" />
  <img src="images/settings_menu_screenshot.png" alt="Settings Menu" width="45%" />

## Key Features

- **Custom GUI with `customtkinter`:** The application utilizes the **`customtkinter`** library to provide a modern and customizable graphical user interface (GUI), enhancing the visual appeal and user experience.


- **Secure User Authentication:**

  - **Password Hashing:** User passwords are securely hashed using the **`sha256`** algorithm before being stored, ensuring that plain-text passwords are never saved.
  - **User Management:** Includes the ability to create new users, with a default administrator account created if no users exist in the system.
  - **Password Visibility Toggle:** Users can toggle the visibility of their password input with a single click, enhancing usability without compromising security.
 

- **Responsive Design:** The application is designed to fit a fixed window size, ensuring that the layout remains consistent across different screen resolutions.


- **Customizable Appearance:**

  - **Dark Mode:** The GUI is set to a dark mode by default, providing a modern and eye-friendly appearance.
  - **Custom Fonts and Icons:** Various UI elements, such as buttons and input fields, feature custom fonts and icons to match the overall theme of the application.
 

- **Persistent User Data:**

  - **Local Storage:** User data is stored locally in a JSON file, allowing the application to maintain user credentials across sessions.
  - **Error Handling:** The application gracefully handles missing or corrupt user data files, automatically creating a new user database if needed.
 

- **Admin Panel with Settings:**

  - **Admin-Only Access:** The settings menu is accessible exclusively through the admin panel, allowing only authorized users to make critical changes.
  - **Settings Management:** Admin users can access various settings, potentially including user management, theme changes, and system configurations (depending on implementation).


- **Visual Feedback and Accessibility:**

  - **Hover Effects:** Interactive elements, such as buttons, provide visual feedback on hover, improving accessibility and user interaction.
  - **Consistent Iconography:** The application uses a consistent set of icons for common actions like showing/hiding passwords, navigating, and accessing settings.


- **Extensible and Modular Design:**

  - **Easily Extendable:** The codebase is structured in a modular fashion, making it easy to extend or customize the application for different use cases.
  - **Resource Management:** External resources like images and icons are managed efficiently, ensuring the application's responsiveness and performance.


## How To Use

## Download

## License

[CTk-Login-Menu](https://github.com/Master-Programmer-2010/CTk-Login-Menu) is licensed under the `MIT License`.

See [LICENSE](./LICENSE) for details.
