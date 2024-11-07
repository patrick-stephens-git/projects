## Import Module Requirements:
import pandas as pd

example_list = [1, 2, 3]
email_data = pd.DataFrame(example_list, columns=['count']).to_html()