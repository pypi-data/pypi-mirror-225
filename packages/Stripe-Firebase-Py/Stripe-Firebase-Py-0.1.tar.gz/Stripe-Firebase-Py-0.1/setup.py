from setuptools import setup, find_packages

# Read the content of README.md
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="Stripe-Firebase-Py",
    version="0.1",
    packages=find_packages(),
    py_modules=["stripe_models"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    install_requires=[
        # Add dependencies here
        "stripe",
        "google-cloud-firestore"
    ]

    #    entry_points={
    #        'console_scripts': [
    #            'stripe_models=stripe_models:main',  # If you have a 'main' function in your script
    #        ],
    #    },
)
