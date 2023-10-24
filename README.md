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

```
IQ-10
├─ README.md
├─ config
├─ src
│  └─ app
│     ├─ backend
│     │  ├─ README.md
│     │  ├─ api
│     │  │  ├─ __init__.py
│     │  │  ├─ api_key_generation
│     │  │  │  ├─ __init__.py
│     │  │  │  └─ generate_api_key.py
│     │  │  ├─ auth
│     │  │  │  ├─ __init__.py
│     │  │  │  └─ auth_user.py
│     │  │  ├─ orders
│     │  │  │  ├─ __init__.py
│     │  │  │  └─ get_orders.py
│     │  │  ├─ products
│     │  │  │  ├─ __init__.py
│     │  │  │  └─ get_products.py
│     │  │  ├─ shipments
│     │  │  │  ├─ __init__.py
│     │  │  │  ├─ orders.py
│     │  │  │  └─ shipments.py
│     │  │  ├─ store
│     │  │  │  ├─ __init__.py
│     │  │  │  └─ session_store.py
│     │  │  ├─ stores
│     │  │  │  ├─ __init__.py
│     │  │  │  └─ get_stores.py
│     │  │  ├─ users
│     │  │  │  ├─ __init__.py
│     │  │  │  └─ get_users.py
│     │  │  └─ vendors
│     │  │     ├─ __init__.py
│     │  │     └─ get_vendors.py
│     │  ├─ global_data.py
│     │  ├─ requirements.txt
│     │  └─ setup.py
│     └─ client
│        ├─ app.py
│        └─ style.css
└─ tests
   ├─ getpages.py
   ├─ test.py
   ├─ test_api_key_generator.py
   ├─ test_auth.py
   ├─ test_orders.py
   ├─ test_products.py
   ├─ test_shipments.py
   ├─ test_stores.py
   ├─ test_users.py
   └─ test_vendors.py

```
