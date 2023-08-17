# Football Fake Data - in development

[![PyPI Version](https://img.shields.io/pypi/v/fake-footballer.svg)](https://pypi.org/project/fake-footballer/)
[![License](https://img.shields.io/pypi/l/fake-footballer.svg)](https://github.com/your-username/fake-footballer/blob/main/LICENSE)

Generate fake footballer data with this Python package.

## Installation

You can install the package using pip:

```
pip install footballtestdata
```
## Usage

Import the FootballerGenerator class and other necessary modules to generate fake footballer data:

```
from footballtestdata import FootballerGenerator, position
from footballtestdata.data import ENG, ITA, SPA, GER
```

Initialize the FootballerGenerator object with the desired data for a specific country:
```
country = 'ENG'
footballer_generator = FootballerGenerator(ENG[0], ENG[1], ENG[2], ENG[3], position)
```
Generate fake footballer data:
```
num_footballers = 10
fake_footballers = [footballer_generator.generate_fake_footballer(country) for _ in range(num_footballers)]
```
Create a pandas DataFrame from the generated data:
```
import pandas as pd
df = pd.DataFrame(fake_footballers)
```
Save the DataFrame to an Excel file:
```
filename = f'fake_{country}_footballers.xlsx'
df.to_excel(filename, index=False)
```
Extended use case:
```
# This is the use example of footballer_gen. First do all necessary imports: 

import pandas as pd
from footballtestdata.data import ENG, ITA, SPA, GER, position
from footballtestdata.footballer_gen import FootballerGenerator

# Map the user's choice to the country code
country_mapping = {
    '1': 'ENG',
    '2': 'ITA',
    '3': 'SPA',
    '4': 'GER'
}

datasets = []  # List to store generated datasets

while True:
    print("Available countries:")
    print("1. England (ENG)")
    print("2. Italy (ITA)")
    print("3. Spain (SPA)")
    print("4. Germany (GER)")

    country_choice = input("Enter the number corresponding to the desired country.\nLater you will be asked the same question once again if you want to create a data set with players from different countries (or 'q' to quit): ")

    if country_choice.lower() == 'q':
        break  # Exit the loop if user enters 'q'

    # Validate the user's choice
    if country_choice not in country_mapping:
        print("Invalid country choice. Please try again.")
        continue  # Continue to the next iteration of the loop

    country = country_mapping[country_choice]

    # Set up the FootballerGenerator based on the chosen country
    if country == 'ENG':
        footballer_generator = FootballerGenerator(ENG[0], ENG[1], ENG[2], ENG[3], position)
    elif country == 'ITA':
        footballer_generator = FootballerGenerator(ITA[0], ITA[1], ITA[2], ITA[3], position)
    elif country == 'SPA':
        footballer_generator = FootballerGenerator(SPA[0], SPA[1], SPA[2], SPA[3], position)
    elif country == 'GER':
        footballer_generator = FootballerGenerator(GER[0], GER[1], GER[2], GER[3], position)

    # Prompt the user to enter the number of fake footballers to generate
    num_footballers = input("Enter the number of fake footballers to generate: ")

    # Validate the user's input for the number of footballers
    if not num_footballers.isdigit() or int(num_footballers) <= 0:
        print("Invalid number of footballers. Please try again.")
        continue  # Continue to the next iteration of the loop

    num_footballers = int(num_footballers)

    # Generate fake footballers
    fake_footballers = [footballer_generator.generate_fake_footballer(country) for _ in range(num_footballers)]

    datasets.append(pd.DataFrame(fake_footballers))  # Add the generated dataset to the list

# Concatenate and save all datasets to a single Excel file
filename = 'fake_footballers.xlsx'
final_dataset = pd.concat(datasets)
final_dataset.to_excel(filename, index=False)
print(f"Fake footballers data saved to {filename}:\n")
print(final_dataset)

```

For more usage examples and customization options, please refer to the documentation.

## Documentation
For detailed documentation, refer to the official documentation.

## Contributing
Contributions are welcome! If you would like to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make the necessary changes and commit them.
4. Open a pull request on the main branch.
5. Please review the contribution guidelines for more details.

## License
This project is licensed under the MIT License.
