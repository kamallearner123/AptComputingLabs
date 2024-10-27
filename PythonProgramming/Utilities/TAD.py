
# pip install pandas openpyxl


import pandas as pd
import json
from openpyxl import Workbook
import os

# Load JSON data for features and non-functional requirements
def load_features_and_non_functionalities(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    features = list(map(lambda d:d["name"], data['features']))
    non_functionalities =list(map(lambda d:d["name"], data['non_functionalities']))
    print(features)
    print(non_functionalities)
    return features, non_functionalities

# Generate TTA and FIA tables
def generate_tta_fia_tables(features,non_functionalities):
    # TTA and FIA tables
    tta_table = pd.DataFrame(index=features, columns=non_functionalities)
    fia_table = pd.DataFrame(index=features, columns=features)

    # Fill tables with "Yes" or blank based on interactions (for example, setting default as "Yes")
    tta_table.fillna("Yes", inplace=True)
    fia_table.fillna("Yes", inplace=True)

    return tta_table, fia_table

# Generate PTS sheet based on TTA and FIA
def generate_pts_sheet(tta_table, fia_table):
    pts_data = []
    pts_id_counter = 1
    
    print(tta_table)
    
    # Get interactions marked "Yes" in TTA table and add to PTS sheet
    for feature in tta_table.index:
        for non_functionality in tta_table.columns:
            if tta_table.loc[feature, non_functionality] == "Yes":
                pts_data.append([f"PTS-{pts_id_counter}", f"{feature} - {non_functionality} interaction"])
                pts_id_counter += 1

    # Get interactions marked "Yes" in FIA
    for feature in tta_table.index:
        for feature2 in fia_table.columns:
            if feature != feature2 and fia_table.loc[feature, feature2] == "Yes":
                pts_data.append([f"PTS-{pts_id_counter}", f"{feature} - {feature2} interaction"])
                pts_id_counter += 1

    pts_df = pd.DataFrame(pts_data, columns=["PTS ID", "PTS Description"])
    return pts_df

# Generate Test Case sheet template
def generate_test_case_sheet(pts_df):
    # Add one 
    test_case_columns = ["PTS ID", "PTS Description", "Test Case ID", "Feature", "Scenario", "Preconditions", "Steps", "Expected Result", "Actual Result", "Status"]

    test_cases = []

    for index, row in pts_df.iterrows():
        # Prepare a dictionary for each test case row
        # prepare list with values for each column and append to the dataframe

        test_case = [row["PTS ID"], row["PTS Description"], f"TC-{index + 1}", row["PTS Description"], "Sample Scenario", "Sample Preconditions", "Sample Steps", "Sample Expected Result", "", "FAIL"]

        # test_case = {
        #     "PTS ID": row["PTS ID"],
        #     "PTS Description": row["Description"],
        #     "Test Case ID": f"TC-{index + 1}",
        #     "Feature": row["Description"].split(" - ")[0],  # Extract feature from the description
        #     "Scenario": "Sample Scenario",                  # Placeholder scenario
        #     "Preconditions": "Sample Preconditions",        # Placeholder preconditions
        #     "Steps": "Sample Steps",                        # Placeholder steps
        #     "Expected Result": "Sample Expected Result",    # Placeholder expected result
        #     "Actual Result": "",                            # Empty field for actual result
        #     "Status": "FAIL"                                # Default status as FAIL
        # }
        # Add test_case dictionary with columns as keys to the dataframe
        test_cases.append(test_case)
        
    test_case_df = pd.DataFrame(test_cases, columns=test_case_columns)
    # Create another sheet to find the test report with number of test cases and number of test cases passed and failed for each feature and non functionality.
    # "Test report" sheet should get updated automatically based on the test cases status in "Test Cases" sheet.

    test_report_columns = ["Feature", "Non Functionality", "Total Test Cases", "Test Cases Passed", "Test Cases Failed"]
    test_report_df = pd.DataFrame(columns=test_report_columns)


    return test_case_df,test_report_df

# Main function to execute script
def main(json_file, output_file):
    # Load features and non-functional requirements
    features, non_functionalities = load_features_and_non_functionalities(json_file)

    # Generate TTA and FIA tables
    tta_table, fia_table = generate_tta_fia_tables(features, non_functionalities)
    # Write these tables with index as first column to an Excel file with sheets TTA and FIA
    with pd.ExcelWriter("test_document_tmp.xlsx", engine="openpyxl") as writer:
        tta_table.to_excel(writer, sheet_name="TTA", index_label="Feature")
        fia_table.to_excel(writer, sheet_name="FIA", index_label="Feature")

    # Wait for user input to proceed
    input("Press Enter to generate PTS and Test Cases...")

    # Generate PTS sheet
    # Read excel file and get tta_table and fia_table from the excel file from sheet TTA and FIA
    tta_table = pd.read_excel("test_document_tmp.xlsx", sheet_name="TTA", index_col="Feature")
    fia_table = pd.read_excel("test_document_tmp.xlsx", sheet_name="FIA", index_col="Feature")
    pts_df = generate_pts_sheet(tta_table, fia_table)

    # Generate Test Case sheet
    test_case_df, test_report_df = generate_test_case_sheet(pts_df)

    # Create a new Excel workbook and add sheets
    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        tta_table.to_excel(writer, sheet_name="TTA")
        fia_table.to_excel(writer, sheet_name="FIA")
        pts_df.to_excel(writer, sheet_name="PTS", index=False)
        test_case_df.to_excel(writer, sheet_name="Test Cases", index=False)
        test_report_df.to_excel(writer, sheet_name="Test Report", index=False)

    print(f"Excel file '{output_file}' created successfully with TTA, FIA, PTS, and Test Cases sheets.")

# Run the script with the specified JSON file and output file
if __name__ == "__main__":
    json_file = "features.json"  # Replace with your JSON input file path
    
    # Take back up of the file test_document.xlsx before running the script and rename it with timestamp
    # Rename the file if it already exists othrwise no need to rename
    if os.path.exists("test_document.xlsx"):
        os.rename("test_document.xlsx", "test_document_" + str(os.path.getmtime("test_document.xlsx")) + ".xlsx")
    output_file = "test_document.xlsx"  # Output Excel file path
    main(json_file, output_file)
