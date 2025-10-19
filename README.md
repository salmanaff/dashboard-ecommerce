# E-Commerce Performance & RFM Analysis
A Streamlit dashboard for analyzing key e-commerce trends, revenue drivers, and customer lifetime value using RFM modeling.

## Business Problem
The e-commerce business requires translating high volumes of transactional data into fast, reliable business insights. Manual data aggregation and reporting were time-consuming, leading to delayed decision-making regarding inventory, marketing spend, and customer engagement.
The key problems addressed were:
1. **Lack of Real-Time Visibility:** No unified view to monitor daily orders, revenue trends, and product performance.
2. **Untargeted Marketing:** Inability to identify and segment high-value, at-risk, or new customers for cost-effective, personalized retention and up-sell campaigns.
3. **Operational Blind Spots:** Poor understanding of sales concentration (e.g., high reliance on São Paulo (SP)), popular payment methods (75% on credit card), and optimal order times.

## Methodology
### Data Engineering
**Python** and **Pandas** for ETL, data cleaning, aggregation, and feature engineering.
### Statistical Modelling
**RFM (Recency, Frequency, Monetary) Analysis** for customer segmentation and lifetime value estimation.
### Visualization and Deployment
**Streamlit** for building the interactive, web-deployed dashboard.  
**Matplotlib** and **seaborn** for generating charts.

## Insight
- **High Category Performance:** bed_bath_table is the top-selling category, while security_and_services is the worst.
- **Geographic Concentration:** Over $40\%$ of all customers and orders originate from the state of São Paulo (SP).
- **Payment Method:** $75\%$ of all transactions rely on credit_card.
- **RFM Segmentation:** High-value customers are identified by their high Frequency and Monetary scores.

## Next Steps
1. **Predictive Modeling Integration**  
Implement a basic customer churn prediction model and integrate its output as a new feature within the Streamlit dashboard, allowing for proactive intervention.
2. **Live Data Integration**  
Transition the current static dataset to a cloud-based SQL database (e.g., PostgreSQL or BigQuery) to allow the Streamlit dashboard to pull and display near real-time data.
3. **Sentiment Analysis**  
Integrate customer review data and perform natural language processing (NLP) to generate a "Product Sentiment" score for each category, adding qualitative depth to the performance analysis.
4. **A/B Test Monitoring**  
Add a dedicated page to monitor the results of marketing and pricing A/B tests, centralizing all key decision-making data in one application.



## Setup Environment
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install pandas matplotlib seaborn jupyter streamlit babel
```

## Run steamlit app
```
streamlit run dashboard.py
```
