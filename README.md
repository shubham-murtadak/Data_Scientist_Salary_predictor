
# 💼 SalaryPredict AI - Data Scientist Salary Predictor using Ml

A comprehensive tool designed to estimate data science salaries based on job descriptions. This project helps data scientists negotiate better salaries when searching for a job.

## 🚀 Project Overview
- **Goal**: Build a salary estimator for data scientists to help them assess potential salaries based on job listings.
- **Data**: Scraped over 1000 job descriptions from Glassdoor using Selenium and Python.
- **Tech Stack**: Engineered key features, optimized machine learning models, and built an API for user interaction.
- **Outcome**: Achieved a highly accurate salary prediction tool using machine learning techniques like Random Forest and Lasso Regression.

---

## 📦 Code and Resources Used

- **Python Version**: 3.11.3
- **Packages**:
  - Data processing: `pandas`, `numpy`
  - Visualization: `matplotlib`, `seaborn`
  - Machine Learning: `sklearn`
  - Web scraping: `selenium`, `BeautifulSoup`
  - Web framework: `flask`
  - Utilities: `pickle`, `json`
  
- **Setup**:  
  To install all dependencies, use:
  ```bash
  pip install -r requirements.txt
  ```

---

## 🌐 Web Scraping

We developed a web scraper to extract over 1000 job postings from Glassdoor. The scraper captured the following details for each job:

- Job Title
- Salary Estimate
- Job Description
- Rating
- Company Information (Name, Size, Location, Headquarters, Founded Date)
- Job Information (Type of Ownership, Industry, Sector, Revenue, Competitors)

---

## 🧹 Data Cleaning

To ensure the data was usable for the model, several cleaning operations were performed:

- Extracted numerical values from salary estimates.
- Separated salary into employer-provided salary and hourly wages.
- Removed entries with missing salary information.
- Created columns for specific job skills (Python, R, Excel, AWS, Spark).
- Parsed company rating and location details.
- Calculated the company's age from the founding year.
- Created simplified job titles and seniority levels.
- Added a column for job description length.

---

## 📊 Exploratory Data Analysis (EDA)

In this step, we analyzed distributions of various features and examined the relationships between variables. Below are some insights gained through pivot tables and visualizations:

### Salary by Job Title
![Salary by Position](https://github.com/shubham-murtadak/Data_Scientist_Salary_predictor/blob/main/images/salary_by_job_title.PNG)

### Job Opportunities by State
![Job Opportunities by State](https://github.com/shubham-murtadak/Data_Scientist_Salary_predictor/blob/main/images/positions_by_state.png)

### Correlation Between Features
![Correlations](https://github.com/shubham-murtadak/Data_Scientist_Salary_predictor/blob/main/images/correlation_visual.png)

---

## 🛠️ Model Building

We transformed categorical variables into dummy variables and split the data into training (80%) and testing (20%) sets. Three models were evaluated based on **Mean Absolute Error (MAE)**:

1. **Multiple Linear Regression** – Baseline model
2. **Lasso Regression** – Helps reduce overfitting by penalizing irrelevant features
3. **Random Forest** – Robust against overfitting due to data sparsity

---

## 🏆 Model Performance

Among the models, **Random Forest** outperformed others in predicting salaries:

| Model                  | MAE (Mean Absolute Error) |
|------------------------|---------------------------|
| **Random Forest**       | **11.22**                 |
| Linear Regression       | 18.86                     |
| Ridge Regression        | 19.67                     |

---

## 🔥 Productionization

To deploy the model, a simple API was created using Flask. The API allows users to submit job descriptions and receive an estimated salary based on the input features.

```bash
# Running the Flask application locally
python app.py
```

The API takes in job details like title, skills required, location, and company size, and returns a salary prediction.

---

## 📚 How to Run This Project Locally

1. **Clone the repository**:
   ```bash
   git clone https://github.com/shubham-murtadak/Data_Scientist_Salary_predictor.git
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask app**:
   ```bash
   python app.py
   ```

4. **Access the web app**:
   Open your browser and go to `http://127.0.0.1:5000/`

---

## ✨ Features

- **Web Scraping**: Efficiently extracts job data from Glassdoor.
- **Data Preprocessing**: Cleans and prepares data for modeling.
- **Salary Estimation**: Predicts salaries using state-of-the-art machine learning models.
- **Interactive API**: Flask-powered API allows real-time salary estimation based on job descriptions.

---

## 📈 Results

The Random Forest model provided the best predictions, helping users estimate their salary expectations. This project can be expanded to scrape more jobs, use more features, and enhance the model.

---

## 🤝 Contributions

Feel free to contribute to this project by opening an issue or submitting a pull request.

---

### Contact

For any inquiries, reach out to:
- **Shubham Murtadak** - shubhammurtadak022@gmail.com

---

### License

This project is licensed under the MIT License.

---
