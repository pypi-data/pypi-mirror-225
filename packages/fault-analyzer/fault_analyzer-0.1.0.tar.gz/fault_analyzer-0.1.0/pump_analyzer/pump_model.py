import fault_analyzer
from fault_analyzer import PumpFailureAnalyzer


file_path = "d:/Work_data/pump_old_data/pump_old_data.xlsx"
analyzer = PumpFailureAnalyzer(file_path)
analyzer.detect_failure()
analyzer.save_results_to_csv("d:/Work_data/pump_old_data/your_output_file.csv")
analyzer.visualize_data()