# Project Name: CS-Cart API Integration with Streamlit

This project demonstrates the integration of the CS-Cart API with a Streamlit web application. CS-Cart is an e-commerce platform that provides a powerful API for interacting with its functionality programmatically. Streamlit is a Python library for building interactive web applications.

## Getting Started

To get started with this project, follow the instructions below.

### Prerequisites

- Python 3.6+
- CS-Cart account with API access
- API key and email from CS-Cart

### Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/radarapps/IQ-10.git
   cd IQ-10
   ```

2. Create a virtual environment (optional but recommended):

   ```shell
   python3 -m venv env
   source env/bin/activate
   ```

3. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```

4. Set up your CS-Cart API credentials:

   - Open the `.env.example` file and update the `API_KEY` and `API_SECRET` fields with your CS-Cart API key and secret.

## Usage

To run the Streamlit web application, use the following command:

```shell
streamlit run app.py
```

Once the application is running, open your web browser and navigate to the provided local URL. You should see the CS-Cart API integration interface, where you can perform various operations using the CS-Cart API.

## Features

The CS-Cart API integration with Streamlit provides the following features:

- Retrieve products from CS-Cart
- Update product details
- Create new products
- Delete products
- Get order details
- Update order status
- Create new orders
- Retrieve customer details
- Update customer information

## Contributing

Contributions to this project are welcome. If you find any issues or want to add new features, please submit a pull request. Make sure to follow the existing code style and include appropriate tests.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- CS-Cart API documentation: [https://docs.cs-cart.com/](https://docs.cs-cart.com/)
- Streamlit documentation: [https://docs.streamlit.io/](https://docs.streamlit.io/)

## Contact

If you have any questions or suggestions regarding this project, feel free to contact the project maintainer:

- Name: Bhavesh Choudhary
- Email: probhavsh@gmail.com