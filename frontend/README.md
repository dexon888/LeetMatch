# LeetMatch

LeetMatch is a web application that recommends similar LeetCode problems based on a given problem URL. It leverages a machine learning model trained on a dataset of LeetCode solutions to provide similarity recommendations.

## Features

- **User Authentication**: Sign up and log in using email and password.
- **Problem Recommendations**: Enter a LeetCode problem URL to receive a list of similar problems.
- **Interactive UI**: Recommendations are displayed as clickable buttons for easy navigation.
- **Responsive Design**: Optimized for various screen sizes.

## Technologies Used

- **Frontend**: React.js, Tailwind CSS
- **Backend**: Node.js, Express.js
- **Authentication**: Firebase Authentication
- **Database**: Firebase Firestore (for user data)
- **API**: Custom recommendation API

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/YOUR_GITHUB_USERNAME/LeetMatch.git
    cd LeetMatch
    ```

2. **Install dependencies**:

    - For the frontend:
      ```bash
      cd frontend
      npm install
      ```

    - For the backend:
      ```bash
      cd backend
      npm install
      ```

3. **Setup Firebase**:
    - Create a Firebase project at [Firebase Console](https://console.firebase.google.com/).
    - Enable Email/Password authentication in the Firebase Authentication settings.
    - Obtain your Firebase config object from the Firebase Console and replace the placeholder values in `frontend/src/firebase.js`.

4. **Run the application**:

    - Start the backend server:
      ```bash
      cd backend
      npm start
      ```

    - Start the frontend development server:
      ```bash
      cd frontend
      npm start
      ```

    The application should now be running at `http://localhost:3000`.

## Usage

1. **Sign Up / Log In**:
    - Use the authentication form to sign up for a new account or log in with an existing account.

2. **Get Recommendations**:
    - Enter a LeetCode problem URL in the provided input field and click "Get Recommendations".
    - The application will display a list of similar problems as clickable buttons.

3. **Log Out**:
    - Use the "Sign Out" button to log out of your account.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature/your-feature-name`.
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, please contact [YOUR_EMAIL@example.com].

