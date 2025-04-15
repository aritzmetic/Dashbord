import os
import pandas as pd

def get_dataset_path(filename="Cleaned_School_DataSet.csv"):
    return os.path.join(os.path.dirname(__file__), 'static', filename)

def fetch_enrollment_data_from_csv(file_path):
    try:
        df = pd.read_csv(file_path)

        # Calculate total male and female enrollments by summing across grade levels
        total_male = df['K Male'].sum() + df['G1 Male'].sum() + df['G2 Male'].sum() + \
                     df['G3 Male'].sum() + df['G4 Male'].sum() + df['G5 Male'].sum() + \
                     df['G6 Male'].sum() + df['Elem NG Male'].sum() + df['G7 Male'].sum() + \
                     df['G8 Male'].sum() + df['G9 Male'].sum() + df['G10 Male'].sum() + \
                     df['JHS NG Male'].sum() + df['G11 ACAD - ABM Male'].sum() + \
                     df['G11 ACAD - HUMSS Male'].sum() + df['G11 ACAD STEM Male'].sum() + \
                     df['G11 ACAD GAS Male'].sum() + df['G11 ACAD PBM Male'].sum() + \
                     df['G11 TVL Male'].sum() + df['G11 SPORTS Male'].sum() + \
                     df['G11 ARTS Male'].sum() + df['G12 ACAD - ABM Male'].sum() + \
                     df['G12 ACAD - HUMSS Male'].sum() + df['G12 ACAD STEM Male'].sum() + \
                     df['G12 ACAD GAS Male'].sum() + df['G12 ACAD PBM Male'].sum() + \
                     df['G12 TVL Male'].sum() + df['G12 SPORTS Male'].sum() + \
                     df['G12 ARTS Male'].sum()

        total_female = df['K Female'].sum() + df['G1 Female'].sum() + df['G2 Female'].sum() + \
                       df['G3 Female'].sum() + df['G4 Female'].sum() + df['G5 Female'].sum() + \
                       df['G6 Female'].sum() + df['Elem NG Female'].sum() + df['G7 Female'].sum() + \
                       df['G8 Female'].sum() + df['G9 Female'].sum() + df['G10 Female'].sum() + \
                       df['JHS NG Female'].sum() + df['G11 ACAD - ABM Female'].sum() + \
                       df['G11 ACAD - HUMSS Female'].sum() + df['G11 ACAD STEM Female'].sum() + \
                       df['G11 ACAD GAS Female'].sum() + df['G11 ACAD PBM Female'].sum() + \
                       df['G11 TVL Female'].sum() + df['G11 SPORTS Female'].sum() + \
                       df['G11 ARTS Female'].sum() + df['G12 ACAD - ABM Female'].sum() + \
                       df['G12 ACAD - HUMSS Female'].sum() + df['G12 ACAD STEM Female'].sum() + \
                       df['G12 ACAD GAS Female'].sum() + df['G12 ACAD PBM Female'].sum() + \
                       df['G12 TVL Female'].sum() + df['G12 SPORTS Female'].sum() + \
                       df['G12 ARTS Female'].sum()

        total_enrollments = total_male + total_female
        number_of_schools = df['BEIS School ID'].nunique()
        regions_with_schools = df['Region'].nunique()
        # Assuming each unique combination of grade level columns represents a year level
        number_of_year_levels = 13 # Based on the K to G12 structure

        enrollment_data = {
            'totalEnrollments': int(total_enrollments),
            'maleEnrollments': int(total_male),
            'femaleEnrollments': int(total_female),
            'numberOfSchools': int(number_of_schools),
            'regionsWithSchools': int(regions_with_schools),
            'numberOfYearLevels': int(number_of_year_levels)
        }
        return enrollment_data
    except FileNotFoundError as e:
        print(f"Error: File not found at {file_path}: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == '__main__':
    file_path = get_dataset_path()
    data = fetch_enrollment_data_from_csv(file_path)
    if data:
        print(data)