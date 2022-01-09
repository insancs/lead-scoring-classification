# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %% [markdown]
# # Problem Statement
# %% [markdown]
# ## Context
# %% [markdown]
# Sebuah perusahaan pendidikan bernama X Education menjual kursus online kepada para profesional industri. Pada hari tertentu, banyak profesional yang tertarik dengan kursus tersebut denga membuka situs web mereka dan mencari kursus.
# 
# Perusahaan memasarkan kursusnya di beberapa situs web dan mesin pencari seperti Google. Setelah orang-orang ini membuka situs web, mereka mungkin mencari kursus atau mengisi formulir untuk kursus atau menonton beberapa video. Ketika orang-orang ini mengisi formulir yang memberikan alamat email atau nomor telepon mereka, mereka diklasifikasikan sebagai "Prospek". Selain itu, perusahaan juga mendapatkan arahan melalui referensi sebelumnya. Setelah prospek ini diperoleh, karyawan dari tim penjualan mulai menelepon, menulis email, dan lain-lain. Melalui proses ini, beberapa prospek dikonversi sementara sebagian besar tidak. Tingkat konversi prospek pada pendidikan X adalah sekitar 30%.
# 
# Sekarang, meskipun X Education mendapatkan banyak prospek, tingkat konversi prospeknya sangat buruk. Misalnya, mereka memperoleh 100 prospek dalam sehari, hanya sekitar 30 di antaranya yang dikonversi. Untuk membuat proses ini lebih efisien, perusahaan ingin mengidentifikasi prospek paling potensial, juga dikenal sebagai "Hot Prospek". Jika mereka berhasil mengidentifikasi kumpulan prospek ini, tingkat konversi prospek akan naik karena tim penjualan sekarang akan lebih fokus untuk berkomunikasi dengan prospek potensial daripada menelepon semua orang.
# 
# Ada banyak prospek yang dihasilkan pada tahap awal, tetapi hanya sedikit dari mereka yang keluar sebagai pelanggan yang membayar. Di tahap ini, Anda perlu memelihara prospek potensial dengan baik (yaitu memperkenalkan prospek tentang produk, terus berkomunikasi, dan lain-lain) untuk mendapatkan konversi prospek yang lebih tinggi.
# 
# X Education ingin memilih prospek yang paling menjanjikan, yaitu prospek yang kemungkinan besar akan dikonversi menjadi pelanggan yang membayar. Perusahaan mengharuskan Anda untuk membangun model di mana Anda perlu menetapkan skor prospek untuk setiap prospek sehingga pelanggan dengan skor prospek yang lebih tinggi memiliki peluang konversi yang lebih tinggi dan pelanggan dengan skor prospek yang lebih rendah memiliki peluang konversi yang lebih rendah. CEO, khususnya, telah memberikan rata-rata target tingkat konversi prospek menjadi sekitar 80%.
# %% [markdown]
# ## Business Goals 
# Buat model untuk menetapkan skor prospek antara 0 sampai 100 untuk setiap prospek yang dapat digunakan oleh perusahaan untuk menargetkan prospek potensial. Skor yang lebih tinggi berarti "Hot Prospek", yaitu kemungkinan besar akan dikonversi sedangkan skor lebih rendah berarti "Cold Prospek" dan tidak akan dikonversi. 
# 
# 
# %% [markdown]
# # Import Libraries

# %%
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import RobustScaler
from sklearn.feature_selection import RFE
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split, cross_validate, StratifiedKFold, GridSearchCV, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, ExtraTreesClassifier, GradientBoostingClassifier, BaggingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.metrics import auc, roc_curve, RocCurveDisplay, precision_recall_curve, PrecisionRecallDisplay
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report 

import joblib
import warnings
warnings.filterwarnings('ignore')
get_ipython().run_line_magic('load_ext', 'autotime')


# %%
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 100)

# %% [markdown]
# # Data Exploration
# %% [markdown]
# Pada tahap ini dilakukan eksplorasi data, seperti dimensi data, tipe data setiap kolom, statistik deskriptif data, mengecek apakah terdapat missing value, dan duplikat data. 
# %% [markdown]
# ## Load Dataset

# %%
# Load csv file
df_lead = pd.read_csv("Lead Scoring.csv")
# Print top five rows
df_lead.head()

# %% [markdown]
# ## Dataframe Information

# %%
# Dataframe dimension
print("Dataframe dimension    :",df_lead.shape)
print("Dataframe size         :",df_lead.size)
print("Number of Row          :",len(df_lead.index))
print("Number of Columns      :",len(df_lead.columns))


# %%
# Dataframe information
df_lead.info()

# %% [markdown]
# ## Statistics Description

# %%
# Statistics description for numerical features
df_lead.describe()


# %%
# Decstiption for categorical columns
df_lead.select_dtypes('object').describe()

# %% [markdown]
# ## Check Null Values

# %%
# number of null values
num_null = df_lead.isnull().sum()

# percentage null values
pct_null = round((num_null/df_lead.shape[0] * 100), 2)

# Create dataframe for number of null value and percentage of null values
df_null = pd.DataFrame({
    'Null Values':num_null,
    'Percentage':pct_null}).reset_index()

# Rename column index to Feature 
df_null.rename(columns={'index':'Features'}, inplace=True)

# Filter only features with null values and sort as descending
df_null = df_null[df_null['Null Values'] > 0].sort_values('Null Values', ascending=False).reset_index(drop=True)
df_null


# %%
# Plotting number of missing data
fig, ax = plt.subplots(figsize=(15,6))

g = sns.barplot(x = 'Features',y='Percentage',data=df_null,ax=ax, 
               palette=sns.color_palette("Blues_d", n_colors=13, desat=1))

x = np.arange(len(df_null['Features']))
y = df_null['Percentage']

for i, v in enumerate(y):
    ax.text(x[i]-0.3, v+2, str(v)+'%', fontsize = 12, color='gray', fontweight='bold')
    

text = '''
There are 17 (45.94%) features that have missing value.

Feature with more than 30% missing value is 
Lead Quality, Asymmetrique Profile Score, Asymmetrique Activity Score,
Asymmetrique Profile Index, Asymmetrique Activity Index, and Tags.
'''
ax.text(0,65,text,horizontalalignment='left',color='black',fontsize=14,fontweight='normal')
ax.set_title('Missing values distribution', color='black', fontsize=20, fontweight='bold')
ax.set_xticklabels(ax.get_xticklabels(),rotation=90)
ax.set_ylim(0,100)
plt.show()

# %% [markdown]
# Dari hasil diatas didapatkan bahwa terdapat 17 feature yang memiliki data null. 
# Terdapat beberapa feature yang memiliki data null lebih dari 30%, yaitu Lead Quality, Asymmetrique Profile Score, Asymmetrique Activity Score, Asymmetrique Profile Index, Asymmetrique Activity Index, dan Tags.
# Maka pada tahap data cleansing nanti kita akan menangani data tersebut.
# %% [markdown]
# ## Check Duplicated Data

# %%
# Check the amount of duplicated data
num_duplicated = df_lead.duplicated().sum()
print(f"Total number of duplicate values : {num_duplicated}")

# %% [markdown]
# Terlihat bahwa data yang kita miliki tidak terdapat data duplikat.
# %% [markdown]
# # Data Cleansing
# %% [markdown]
# Pada tahap ini lakukan pembersihan data, mulai dari handling missing value, inconsistent data, kardinalitas data, outliers, dan konversi  tipe data setiap feature sesuai dengan seharusnya.
# %% [markdown]
# ## Handling Missing Values and Inconsistent Data
# %% [markdown]
# Terdapat beberapa skenario yang akan kita lakukan pada handling missing value ini : <br>
# - Prospect ID & Lead Number adalah dua variabel yang hanya menunjukkan nomor ID Orang yang Dihubungi & dapat dihilangkan
# - Feature  seperti Lead Quality, Tags, Asymmetrique scores dan feature profile (Lead Profile) dibuat oleh tim penjualan setelah mereka menghubungi calon prospek. Feature ini tidak akan tersedia untuk pembuatan model karena fitur ini tidak akan tersedia sebelum prospek dihubungi oleh tim penjualan. Maka feature ini dapat kita hilangkan.
# - Last Notable Activity adalah feature perantara yang merupakan pembaruan saat perwakilan tim penjualan berhubungan dengan pemimpin. Dengan demikian, kita juga dapat menghapus kolom ini.
# - Hapus feature yang memiliki Nilai Null lebih dari 30%.
# - Feature dengan data null antara 10% sampai 30% akan dilakukan pengisian data.
# - Feature dengan data null kurang dari 10% akan kita lakukan penghapusan karena tidak akan terlalu berpengaruh pada sebagian data.
# - Kategori pada setiap feature yang memiliki frekuensi kecil dapat digabungkan menjadi satu kategori.

# %%
# List of unnecessary columns
col_drop = [
    'Prospect ID','Lead Number','Lead Profile','Lead Quality',
    'Asymmetrique Profile Score','Asymmetrique Activity Score',
    'Asymmetrique Activity Index','Asymmetrique Profile Index',
    'Tags','Last Notable Activity']

# Remove unnecessary columns
df_lead.drop(col_drop, axis=1, inplace=True)


# %%
# categorical columns
cat_col= list(df_lead.select_dtypes(exclude='number').columns)
# numerical columns
num_col = list(df_lead.select_dtypes('number').columns)

print(f'CATEGORICAL FEATURES {cat_col}')
print(f'\nNUMERICAL FEATURES {num_col}')


# %%
# Number of null values each features
df_null

# %% [markdown]
# ### Categorical Features
# %% [markdown]
# #### Lead Source

# %%
# Number of category for Lead Source feature
df_lead['Lead Source'].value_counts()

# %% [markdown]
# Kita akan ubah kategori yang tidak konsisten, yaitu google menjadi Google. KIta juga akan ubah kategori dengan frekuensi rendah menjadi Other.

# %%
# Replace categori with less number of unique to "Other"
df_lead['Lead Source'] = df_lead['Lead Source'].replace(
    ['Click2call', 'Live Chat', 'NC_EDM', 'Pay per Click Ads', 'Press_Release','Social Media', 
    'WeLearn', 'bing', 'blog', 'testone', 'welearnblog_Home', 'youtubechannel'],
    'Other')

# Replace inconsistent data
df_lead['Lead Source'] = df_lead['Lead Source'].replace({'google':'Google'})

# %% [markdown]
# #### Last Activity

# %%
# Number of category for Last Activity feature
df_lead['Last Activity'].value_counts()

# %% [markdown]
# Karena kami tidak yakin apa yang bisa menjadi aktivitas Terakhir, kami akan menggantinya dengan aktivitas paling sering "Email Dibuka". Kami akan menggabungkan nilai Last Activity yang lebih kecil sebagai 'Other'.

# %%
# Replace categori with less number of unique to "Other Activity"
df_lead['Last Activity'].replace([
    'Had a Phone Conversation', 
    'View in browser link Clicked', 
    'Visited Booth in Tradeshow', 
    'Approached upfront',
    'Resubscribed to emails',
    'Email Received',
    'Email Marked Spam'], 'Other Activity', inplace=True)

# %% [markdown]
# #### Country

# %%
# Number of category for Country feature
df_lead['Country'].value_counts(normalize=True)

# %% [markdown]
# Data negara sangat miring (skewed) karena 95% data dipetakan sebagai India. Maka feature Country tidak diperlukan untuk pembuatan model, dan karena X Education adalah platform online, maka feature Country juga tidak akan kita perlukan, maka kita bisa hapus feature tersebut.

# %%
# Remove Country feature
df_lead.drop('Country', axis=1, inplace=True)

# %% [markdown]
# #### Specialization

# %%
# Number of category for Specialization feature
df_lead['Specialization'].value_counts()

# %% [markdown]
# Pada feature Specialization ini bisa jadi prospek tidak memiliki spesialisasi atau mungkin seorang pelajar dan belum memiliki pengalaman kerja, sehingga tidak memasukkan spesialisasi apapun. Maka kita akan membuat kategori baru yaitu 'Other' untuk menggantikan nilai null.

# %%
# Replace wrong value to null value
df_lead['Specialization'].replace({'Select':np.nan}, inplace=True)
# Filling null value to Other
df_lead['Specialization'].fillna('Other', inplace=True)

# %% [markdown]
# #### How did you hear about X Education

# %%
# Number of category for How did you hear about X Education feature
df_lead['How did you hear about X Education'].value_counts()

# %% [markdown]
# Pada feature diatas terdapat kategori yang seharunsnya tidak ada, yaitu Select. Maka kita bisa hapus kategori tersebut. Kita juga akan isi null valeu dengan nilai modus (Online Search). 

# %%
# Replace wrong value with null value
df_lead['How did you hear about X Education'].replace({'Select':np.nan}, inplace=True)
# Filling null value with mode (Online Search) 
df_lead['How did you hear about X Education'].fillna('Online Search', inplace=True)

# %% [markdown]
# #### What is your current occupation

# %%
# Number of category for Occupation feature
df_lead['What is your current occupation'].value_counts(normalize=True)

# %% [markdown]
# Kategori "Unemployed" yang paling dominan dengan 85% dari keseluruhan feature occupation. Jika kita mengisi data dengan "Unemployed" maka data akan menjadi lebih miring (skewed). Bisa jadi prospek tersebut juga tidak ingin menyebutkan pekerjaannya, maka dengan demikian, kami akan mengisi null value dengan "Other".

# %%
# Filling null value with Other
df_lead['What is your current occupation'].fillna('Other', inplace=True)

# %% [markdown]
# #### What matters most to you in choosing a course

# %%
# Number of category for What matters most to you in choosing a course feature
df_lead['What matters most to you in choosing a course'].value_counts()

# %% [markdown]
# Karena datanya miring (skewed) dan didominasi oleh satu kategori, kita bisa menghapus feature ini karena tidak akan berpengaruh pada model kita nantinya.

# %%
# Remove feature
df_lead.drop('What matters most to you in choosing a course', axis=1, inplace=True)

# %% [markdown]
# #### City

# %%
# Number of category for City feature
df_lead['City'].value_counts(normalize=True)

# %% [markdown]
# Karena ada hampir 40% nilai yang tidak diketahui, kita juga tidak dapat mengisi null value dengan nilai modus karena membuat seluruh data semakin miring (skewed). Juga, X Education adalah platform pengajaran online. Informasi kota tidak akan banyak berguna karena calon siswa dapat memperoleh kursus online dari manapun. Mka kami akan menghapus feature ini.

# %%
# Remove City feature
df_lead.drop('City', axis=1, inplace=True)

# %% [markdown]
# ### Numerical Features
# %% [markdown]
# #### Total Visits

# %%
# Check distribution TotalVisist feature using boxplot
sns.boxplot(data=df_lead, x='TotalVisits')
plt.show()

# %% [markdown]
# #### Page Views Per Visit

# %%
# Check distribution Page Views per Visits feature using boxplot
sns.boxplot(data=df_lead, x='Page Views Per Visit')
plt.show()

# %% [markdown]
# Pada feature TotalVisits dan Page Views per Visits, karena kedua feature tersebut mempunya null value kurang dari 10%, maka kita akan menghapus null value daripada mengisi nilai null tersebut.

# %%
# Remove null value for features with percantage less than 10%
col_drop = df_null[df_null['Percentage'] < 10].columns.to_list()
df_lead.dropna(inplace=True)


# %%
# Make sure there are no features with null values
df_lead.isnull().sum()

# %% [markdown]
# ## Check Number of Unique Values
# %% [markdown]
# Pada tahap ini kita akan melakukan analisis pada feature kategorikal yang hanya mempunyai satu kategori. Jika kondisi tersebut terpenuhi kita akan menghapus feature tersebut karena tidak akan berpengaruh pada model kita nantinya.
# %% [markdown]
# ### Categorical Features

# %%
cat_col = df_lead.select_dtypes('object').columns
# Create dataframe for number of unique values each categorical feature
df_cat_unique = pd.DataFrame(columns=['Feature', 'unique_values'])

# Repeat for each categorical features
for col in cat_col:
    # number of unique value 
    unique = df_lead[col].nunique()

    # Append number of unique values to dataframe
    df_cat_unique = df_cat_unique.append({
        'Feature':col,
        'unique_values':unique
    }, ignore_index=True).sort_values('unique_values', ascending=False)

df_cat_unique


# %%
# List of features that have one unique value
col_drop = list(df_cat_unique[df_cat_unique['unique_values'] == 1]['Feature'])
# Remove features that have one unique value
df_lead.drop(col_drop, axis=1, inplace=True)

# %% [markdown]
# ### Numerical Features

# %%
# Create dataframe for number of unique values each numerical feature
df_num_unique = pd.DataFrame(columns=['Feature', 'unique_values'])

# Repeat for each numerical feature
for col in num_col:
    # number of unique value
    unique = df_lead[col].nunique()

    # Append number of unique values to dataframe
    df_num_unique = df_num_unique.append({
        'Feature':col,
        'unique_values':unique
    }, ignore_index=True).sort_values('unique_values', ascending=False)

df_num_unique

# %% [markdown]
# ## Check Cardinality
# %% [markdown]
# Pada tahap ini kita pastikan kembali bahwa tidak ada feature yang memiliki inconsistent data (khusus feature kategorikal). 

# %%
# List of categorical features
cat_col = df_lead.select_dtypes(exclude='number').columns

# Repeat for each categorical features
for col in cat_col:
    # Print unique value
    print(f'\n{col} : ', df_lead[col].unique())

# %% [markdown]
# # Exploratory Data Analysis
# %% [markdown]
# ## Define Function
# %% [markdown]
# Sebagian besar fitur dalam kumpulan data bersifat kategoris. Mari kita mulai analisis dengan melakukan analisis univariat tersegmentasi pada setiap fitur kategoris. Kami akan melihat plot batang yang akan menunjukkan jumlah total prospek yang dikonversi dan tidak dikonversi di setiap kategori.

# %%
# function for plotting repetitive countplots in univariate categorical analysis on the lead dataset
# This function will create two subplots: 
# 1. Count plot of categorical column w.r.t Converted; 
# 2. Percentage of converted leads within column
def univariate_categorical(feature):
    temp_count = df_lead[feature].value_counts()
    temp_perc = df_lead[feature].value_counts(normalize = True)
    df1 = pd.DataFrame({feature: temp_count.index,'Total Leads': temp_count.values,'% Values': temp_perc.values * 100})
    print(df1)

    # Calculate the percentage of Converted=1 per category value
    cat_perc = df_lead[[feature, 'Converted']].groupby([feature],as_index=False).mean()
    cat_perc["Converted"] = round((cat_perc["Converted"]*100), 2)
    cat_perc.sort_values(by='Converted', ascending=False, inplace=True)

    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(18,7))

    # 1. Subplot 1: Count plot of categorical column
    sns.set_palette("Set2")
    s = sns.countplot(
        ax=ax1, 
        x = feature,
        data=df_lead,
        hue ="Converted",
        order=cat_perc[feature],
        palette=['r','g'])

    # Define common styling
    ax1.set_title(feature, fontdict={'fontsize' : 15, 'fontweight' : 5, 'color' : 'black'}) 
    ax1.set_xlabel(feature, fontsize=20)
    ax1.legend(['Not Converted','Converted'])
    s.set_xticklabels(s.get_xticklabels(),rotation=90)
    
    # 2. Subplot 2: Percentage of defaulters within the categorical column
    x = np.arange(len(cat_perc[feature]))
    y = cat_perc['Converted']
    for i, v in enumerate(y):
        ax2.text(x[i]-0.3, v+1, str(v)+'%', fontsize = 10, color='black', fontweight='bold')

    s = sns.barplot(
        ax=ax2, 
        x = feature, 
        y='Converted', 
        data=cat_perc,
        order=cat_perc[feature])

    ax2.set_title(feature + " ( Converted % )", fontdict={'fontsize' : 15, 'fontweight' : 5, 'color' : 'black'}) 
    ax2.set_ylabel('Percent of Converted leads [%]', fontsize=15)
    ax2.set_xlabel(feature,fontsize=20) 
    s.set_xticklabels(s.get_xticklabels(),rotation=90)
    plt.show()    


# %%
df_lead[['Lead Source', 'Converted']].groupby(['Lead Source'],as_index=False).sum()


# %%
sns.pairplot(df_lead[num_col], hue='Converted')

# %% [markdown]
# #### Insight:
# Pada visualisasi data numerik diatas terlihat bahwa data tidak terdistribusi normal.
# %% [markdown]
# ## Univariate Analysis
# %% [markdown]
# ### Lead Origin

# %%
# Univariate analysis for Lead Origin feature
univariate_categorical('Lead Origin')

# %% [markdown]
# #### Insight :
# - Sebagian besar Prospek berasal dari submission landing page dan sekitar 36% di antaranya dikonversi diikuti oleh API, di mana sekitar 31% dikonversi.
# - Meskipun Lead Origins dari Quick Add Form 100% dikonversi, hanya ada 1 prospek dari kategori tersebut. 
# - Prospek dari Lead Add Form adalah konversi tertinggi berikutnya dalam kategori ini di sekitar 92% dari 718 prospek.
# - Lead Import sangat sedikit dalam hitungan dan tingkat konversi nya juga terendah yaitu sekitar 23%.
# 
# Untuk meningkatkan tingkat konversi prospek secara keseluruhan, kita perlu lebih fokus pada peningkatan konversi prospek asal API dan Submission Landing Page dan menghasilkan lebih banyak prospek dari Lead Add Form.
# %% [markdown]
# ### Lead Source

# %%
# Univariate analysis for Lead Source feature
univariate_categorical('Lead Source')

# %% [markdown]
# #### Insight:
# - Sumber prospek sebagian besar berasal dari Google, dan sekitar 40% prospek dikonversi.
# - Direct Traffic, Olark Chat dan Organic Search sumber prospek terbanyak selanjutnya dengan persentase konversi prospek masing masing 32%, 25% dan 37%.
# - Prospek yang berasal dari referensi memiliki persentase konversi prospek sekitar 91%  dari total 534 prospek.
# - Situs Web Welingak memiliki tingkat konversi prospek hampir 100%, yaitu 98% dari 142 prospek. Opsi ini harus dieksplorasi lebih lanjut untuk meningkatkan konversi prospek.
# 
# Untuk meningkatkan jumlah prospek, inisiatif harus diambil sehingga anggota yang sudah keluar meningkatkan referensi mereka.
# %% [markdown]
# ### Do Not Email

# %%
# Univariate analysis for Do Not Email feature
univariate_categorical('Do Not Email')

# %% [markdown]
# #### Insight
# - Mayoritas orang setuju dengan menerima email (~92%)
# - Orang yang setuju dengan untuk menerima email memiliki tingkat konversi sekitar 40%
# - Orang yang memilih untuk tidak menerima email memiliki tingkat konversi prospek yang lebih rendah (~15%)
# %% [markdown]
# ### Do Not Call

# %%
# Univariate analysis for Do Not Call feature
univariate_categorical('Do Not Call')

# %% [markdown]
# #### Insight
# - Hampir 100% orang setuju dengan menerima panggilan (~99.97%). 
# - Orang yang setuju dengan untuk menerima panggilan memiliki tingkat konversi sekitar 39%.
# - Orang yang memilih untuk tidak menerima email memiliki tingkat konversi prospek sempurna yaitu 100% karena hanya dua prospek.
# %% [markdown]
# ### Last Activity

# %%
# Univariate analysis for Last Activity feature
univariate_categorical('Last Activity')

# %% [markdown]
# #### Insight :
# - Sebagian besar prospek membuka Email mereka sebagai aktivitas terakhir mereka dengan konversi prospek sekitar 36%.
# - Setelah menggabungkan jenis Aktivitas Terakhir yang lebih kecil sebagai "Other Activity", konversi prospek nya sangat tinggi (~74%).
# - Tingkat konversi untuk prospek dengan aktivitas terakhir SMS Terkirim sekitar 63%.
# %% [markdown]
# ### Specialization

# %%
# Univariate analysis for Specialization feature
univariate_categorical('Specialization')

# %% [markdown]
# #### Insight :
# - Sebagian besar prospek belum menyebutkan spesialisasi dan sekitar 28% dari mereka yang dikonversi
# - Prospek dengan Finance Management dan HR Management yang selanjutnya memiliki prospek paling banyak dengan tingkat konversi masing-masing 45% dan 46%.
# - Services Excellence memiliki prospek paling sedikit dengan tingkat konversi sekitar 27%.
# %% [markdown]
# ### How did you hear about X Education

# %%
# Univariate analysis for How did you hear about X Education feature
univariate_categorical('How did you hear about X Education')

# %% [markdown]
# #### Insight :
# - Sebagian besar prospek mengenal X Education dari Pencarian Online (Online Search) dengan total prospek 7894 dan tingkat konversi sekitar 37%.
# -  Word of Mount and Student of Somschool yang selanjutnya memiliki prospek paling banyak dengan tingkat konversi masing-masing sekitar 44% dan 46%.
# - Sebagian kecil mendengar tentang X Education melalui SMS dengan total prospek 23 dengan tingkat konversi sekitar 22%. 
# %% [markdown]
# ### What is your current occupation

# %%
# Univariate analysis for occupation feature
univariate_categorical('What is your current occupation')

# %% [markdown]
# #### Insight :
# - Pengangguran (Unemployee) memiliki jumlah prospek tertinggi dari beberapa pekerjaan lainnya, tetapi tingkat konversiya hanya sekitar 43%.
# - Ibu Rumah Tangga memiliki tingkat konversi tertinggi dengan jumlah 9 prospek.
# - Working Prosession memiliki jumlah prospek ketiga tertinggi dengan tingkat konversi tertinggi kedua yaitu sekitar 92%.
# %% [markdown]
# ### Search

# %%
# Univariate analysis for Search feature
univariate_categorical('Search')

# %% [markdown]
# ### Newspaper Article

# %%
# Univariate analysis for Newspaper Article feature
univariate_categorical('Newspaper Article')

# %% [markdown]
# ### X Education Forums

# %%
# Univariate analysis for X Education Forums feature
univariate_categorical('X Education Forums')

# %% [markdown]
# ### Newspaper

# %%
# Univariate analysis for Newspaper feature
univariate_categorical('Newspaper')

# %% [markdown]
# ### Digital Advertisement

# %%
# Univariate analysis for Digital Advertisement feature
univariate_categorical('Digital Advertisement')

# %% [markdown]
# ### Through Recommendations

# %%
# Univariate analysis for Through Recommendations feature
univariate_categorical('Through Recommendations')

# %% [markdown]
# ### A free copy of Mastering The Interview

# %%
# Univariate analysis for A free copy of Mastering The Interview feature
univariate_categorical('A free copy of Mastering The Interview')

# %% [markdown]
# ## Univariate Analysis : Numerical Features

# %%
num_col.remove('Converted')
num_col


# %%
plt.figure(figsize=(15, 5))
pos = 1

for col in num_col:
    plt.subplot(1, 3, pos)
    sns.histplot(data=df_lead, x=col)
    pos += 1


# %%
plt.figure(figsize=(15, 5))
pos = 1

for col in num_col:
    plt.subplot(1, 3, pos)
    sns.boxplot(data=df_lead, y=col)
    pos += 1

# %% [markdown]
# ## Bivariate Analysis
# %% [markdown]
# ## Remove Feature with Imbalanced Category
# %% [markdown]
# Pada beberapa feature diatas yaitu Do Not Call, Search, Newspaper Article, X Education Forums, Newspaper, Digital Advertisement, dan Through Recommendation terdapat kategori yang sangat tidak seimbang dan sangat jauh perbedaannya, ini tidak akan berpengaruh kepada performa model dan bisa menyebabkan model tidak dapat memprediksi dengan baik. Maka kita akan menghapus feature-feature tersebut.

# %%
# Features with unbalanced category frequency
col_drop = [
    'Do Not Call', 'Search', 'Newspaper Article', 'X Education Forums', 
    'Newspaper', 'Digital Advertisement', 'Through Recommendations']

# Remove features with unbalanced category frequency 
df_lead.drop(col_drop, axis=1, inplace=True)

# %% [markdown]
# ## Correlation Features

# %%
# Correlation heatmap
plt.figure(figsize=(10, 7))
sns.heatmap(df_lead.corr(), annot=True)
plt.show()

# %% [markdown]
# Pada feature numerikal diatas dapat dilihat korelasi setiap feature. TotalVisits dan Page Views per Visits memiliki korelasi positif yang cukup besar. Ini cukup masuk akan karena semakin banyak halaman dilihat pada sebuah website maka semakin tinggi juga waktu yang dihabiskan di sebuah website tersebut. 
# %% [markdown]
# # Feature Engineering
# %% [markdown]
# Pada tahap feature engineering ini akan dilakukan perubahan data menjadi format yang dapat dibaca oleh model ML, rescaling, dan juga feature selection.
# %% [markdown]
# ## Feature Encoding
# %% [markdown]
# Pada tahap ini kita lakukan encoding pada feature karegorikal. Pada feature Do Not Email dan A free copy of Mastering The Interview karena datanya terdapat dua kategori (Yes dan No), maka kita akan ubah menjadi binary encoding. Bisa dengan melakukan replace pada kategori tersebut akan kita bisa lakukan menggunakan Label Encoder. Untuk kali ini kita akan lakukan dengan label encoder.

# %%
col = ['Do Not Email', 'A free copy of Mastering The Interview']

# label encoding
for i in col:
    df_lead[i] = LabelEncoder().fit_transform(df_lead[i])

# %% [markdown]
# ### One-Hot Encoding
# %% [markdown]
# Pada beberapa feature kita akan lakukan one-hot encoding dari pada menggunakan label encoding karena One-Hot encoding lebih cocok pada feature yang memiliki kategori yang banyak.

# %%
# categorical features
one_hot_col = ['Lead Origin', 'Lead Source', 'Last Activity', 'Specialization', 'How did you hear about X Education', 'What is your current occupation']
# one-hot encoding using dummies
df_one_hot = pd.get_dummies(df_lead[one_hot_col])


# %%
# Merge dataframe
df_lead = pd.concat([df_lead, df_one_hot], axis=1)
# Remove categorical features  
df_lead.drop(one_hot_col, axis=1, inplace=True)


# %%
df_lead


# %%
# Reformat data type to integer
for col in df_lead.drop(['TotalVisits', 'Page Views Per Visit'], axis=1).columns:
    df_lead[col] = df_lead[col].astype('int64')

# %% [markdown]
# ## Feature Scaling
# %% [markdown]
# Karena sebelumnya pada feature numerikal terdapat data outliers, maka kita gunakan RobustScaler.

# %%
# Scaling the features
col_scaled = ['TotalVisits', 'Total Time Spent on Website', 'Page Views Per Visit'] 
df_lead[col_scaled] = RobustScaler().fit_transform(df_lead[col_scaled])
df_lead.head()

# %% [markdown]
# ## Feature Selection
# %% [markdown]
# Karena terlalu banyak feature dan hal tersebut dapat menyebabkan model sulit untuk dilatih (memerlukan waktu lama), maka kita akan memilih 20 feature terbaik menggunakan Recursive Feature Elimination (RFE). Untuk classifier yang digunakan pada RFE ini kita gunakan GradientBoostingClassifier.

# %%
# Separate features and target
X = df_lead.drop('Converted', axis=1)
y = df_lead['Converted']


# %%
# Feature selection using RFE
rfe = RFE(estimator=GradientBoostingClassifier(), n_features_to_select=20) # running RFE with 20 variables as output
rfe = rfe.fit(X, y)

col = list(X.columns[rfe.support_])


# %%
# Choose feature from RFE
df_lead = df_lead[col]
df_lead['Converted'] = y
df_lead.head()

# %% [markdown]
# # Sampling Dataset
# %% [markdown]
# ## Separating Train and Test Set 

# %%
# Separate feature and 
X = df_lead.drop('Converted', axis=1)
y = df_lead['Converted']


# %%
# Separate train and test set for modelling
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train and test set dimension
print('Shape of X_train', X_train.shape)
print('Shape of y_train', y_train.shape)
print('Shape of X_test', X_test.shape)
print('Shape of y_test', y_test.shape)

# %% [markdown]
# ## Oversampling Using SMOTE
# %% [markdown]
# Karena pada target yang kita miliki terdapat imbalanced class, maka kita akan melakukan oversampling menggunakan metode SMOTE. Oversampling hanya dilakukan pada data training.

# %%
# Check target distribution 
pd.Series(y_train).value_counts()


# %%
X_train_over, y_train_over = SMOTE().fit_resample(X_train, y_train)

pd.Series(y_train_over).value_counts()

# %% [markdown]
# # Modelling
# %% [markdown]
# Pada tahap modelling kita akan membandingkan beberapa metode yang nantinya kita akan pilih mana model yang menghasilkan performa terbaik. Model dengan performa terbaik akan kita lakukan hyperparameters tuning untuk menghasilkan performa yang lebih baik lagi. 
# %% [markdown]
# ## Choose Best Model

# %%
from sklearn.neural_network import MLPClassifier

# Model assignment
dtc = DecisionTreeClassifier()
rfc = RandomForestClassifier() 
abc = AdaBoostClassifier()
etc = ExtraTreesClassifier() 
gbc = GradientBoostingClassifier() 
bgc = BaggingClassifier()
knn = KNeighborsClassifier() 
logreg = LogisticRegression()
nb = GaussianNB()
svm = SVC()
xgb = XGBClassifier()
mlp = MLPClassifier()

# Assign model to a list
models = [dtc, rfc, abc, etc, gbc, bgc, knn, logreg, nb, svm, xgb, mlp]


model_name = []

# Get Classifier names for every model
for name in models:
    names = str(type(name)).split('.')[-1][:-2]
    # Append classifier names to model_name list
    model_name.append(names)

# %% [markdown]
# ### Cross Validation
# %% [markdown]
# Pada tahap ini kita lakukan training pada seluruh data.

# %%
skfold = StratifiedKFold(n_splits=5, random_state=42, shuffle=True)

# Cross validation for each model
dtc_score = cross_val_score(models[0], X, y, scoring='accuracy', cv=skfold, n_jobs=-1, verbose=1)
rfc_score = cross_val_score(models[1], X, y, scoring='accuracy', cv=skfold, n_jobs=-1, verbose=1)
abc_score = cross_val_score(models[2], X, y, scoring='accuracy', cv=skfold, n_jobs=-1, verbose=1)
etc_score = cross_val_score(models[3], X, y, scoring='accuracy', cv=skfold, n_jobs=-1, verbose=1)
gbc_score = cross_val_score(models[4], X, y, scoring='accuracy', cv=skfold, n_jobs=-1, verbose=1)
bgc_score = cross_val_score(models[5], X, y, scoring='accuracy', cv=skfold, n_jobs=-1, verbose=1)
knn_score = cross_val_score(models[6], X, y, scoring='accuracy', cv=skfold, n_jobs=-1, verbose=1)
logreg_score = cross_val_score(models[7], X, y, scoring='accuracy', cv=skfold, n_jobs=-1, verbose=1)
nb_score = cross_val_score(models[8], X, y, scoring='accuracy', cv=skfold, n_jobs=-1, verbose=1)
svm_score = cross_val_score(models[9], X, y, scoring='accuracy', cv=skfold, n_jobs=-1, verbose=1)
xgb_score = cross_val_score(models[10], X, y, scoring='accuracy', cv=skfold, n_jobs=-1, verbose=1)
mlp_score = cross_val_score(models[11], X, y, scoring='accuracy', cv=skfold, n_jobs=-1, verbose=1)


# %%
# List of score per model
cv_result = [
    dtc_score, rfc_score, abc_score, etc_score, gbc_score, bgc_score, 
    knn_score, logreg_score, nb_score, svm_score, xgb_score, mlp_score]

# Create dataframe for score every k-fold
df_cv_result = pd.DataFrame(cv_result, index=model_name)
df_cv_result


# %%
# Plot cross validation score
sns.set_style('darkgrid')
plt.figure(figsize=(20,10))
sns.lineplot(data=df_cv_result.T)
plt.show()


# %%
# Calculate average for every k-fold validation
cv_mean = []
i = 0
for mean in cv_result:
    mean = cv_result[i].mean()
    cv_mean.append(mean)
    i += 1

# Calculate standard deviation for every k-fold validation
cv_std = []
i = 0 
for mean in cv_result:
    std = cv_result[i].std()
    cv_std.append(std)
    i += 1


# %%
# Average and standard deviation score for each model
df_cv = pd.DataFrame({'score_mean':cv_mean, 'score_std':cv_std}, index=model_name).sort_values(['score_mean', 'score_std'], ascending=False)
df_cv

# %% [markdown]
# Pada eksperimen diatas didapatkan nilai rata-rata akurasi dan standard deviasi dari setiap k-fold validation. GradientBoostingClassifier memiliki performa terbaik dengan rata-rata akurasi mencapai 83% dengan standard deviasi 0.006.
# %% [markdown]
# ### Fit and Evaluation
# %% [markdown]
# Selain dengan menggunakan Cross Validation, saya juga melakukan uji nilai akurasi pada data training dan testing yang bertujuan untuk melihat akurasi saat data training dan testing dan perbedaaannya. Maka di dapatkan hasil sebagai berikut :

# %%
# Create a list to assign a model score
train_score = []
test_score = []
default_models = []

skf = StratifiedKFold(random_state=42, shuffle=True)

# Create dataframe  
df_train_test = pd.DataFrame()
for train_index, test_index in skf.split(X_train_over, y_train_over):
    for i in models:
        # Fit each model
        model = i.fit(X_train_over, y_train_over)
        default_models.append(model)
        # accuracy for training set
        train_score.append(model.score(X_train_over, y_train_over))
        # accuracy for testing set
        test_score.append(model.score(X_test, y_test))


# %%
# average train score model
train_score_dtc = np.sum(train_score[0::12])/len(train_score[0::12]) 
train_score_rfc = np.sum(train_score[1::12])/len(train_score[1::12])
train_score_abc = np.sum(train_score[2::12])/len(train_score[2::12])
train_score_etc = np.sum(train_score[3::12])/len(train_score[3::12])
train_score_gbc = np.sum(train_score[4::12])/len(train_score[4::12])
train_score_bgc = np.sum(train_score[5::12])/len(train_score[5::12])
train_score_knn = np.sum(train_score[6::12])/len(train_score[6::12])
train_score_logreg = np.sum(train_score[7::12])/len(train_score[7::12])
train_score_nbc = np.sum(train_score[8::12])/len(train_score[8::12])
train_score_svm = np.sum(train_score[9::12])/len(train_score[9::12])
train_score_xgb = np.sum(train_score[10::12])/len(train_score[10::12])
train_score_mlp = np.sum(train_score[11::12])/len(train_score[11::12])

# average test score model
test_score_dtc = np.sum(test_score[0::12])/len(test_score[0::12]) 
test_score_rfc = np.sum(test_score[1::12])/len(test_score[1::12])
test_score_abc = np.sum(test_score[2::12])/len(test_score[2::12])
test_score_etc = np.sum(test_score[3::12])/len(test_score[3::12])
test_score_gbc = np.sum(test_score[4::12])/len(test_score[4::12])
test_score_bgc = np.sum(test_score[5::12])/len(test_score[5::12])
test_score_knn = np.sum(test_score[6::12])/len(test_score[6::12])
test_score_logreg = np.sum(test_score[7::12])/len(test_score[7::12])
test_score_nbc = np.sum(test_score[8::12])/len(test_score[8::12])
test_score_svm = np.sum(test_score[9::12])/len(test_score[9::12])
test_score_xgb = np.sum(test_score[10::12])/len(test_score[10::12])
test_score_mlp = np.sum(test_score[11::12])/len(test_score[11::12])


# %%
# List of training accuracy for each model
trainScore = [
    train_score_dtc, train_score_rfc, train_score_abc, train_score_etc, train_score_gbc, train_score_bgc,
    train_score_knn, train_score_logreg, train_score_nbc, train_score_svm, train_score_xgb, train_score_mlp] 

# List of testing accuracy for each model
testScore = [
    test_score_dtc, test_score_rfc, test_score_abc, test_score_etc, test_score_gbc, test_score_bgc,
    test_score_knn, test_score_logreg, test_score_nbc, test_score_svm, test_score_xgb, test_score_mlp] 

# Create a dataframe to store accuracy score
df_avg_score = pd.DataFrame({
    'train score':trainScore,
    'test score':testScore},
    index=model_name)

# Create a new column for the difference in accuracy score 
df_avg_score['difference'] = abs(df_avg_score['train score'] - df_avg_score['test score'])
# Sort accuracy by smallest difference
df_avg_score = df_avg_score.sort_values(['difference'], ascending=True)
df_avg_score

# %% [markdown]
# Terlihat bahwa AdaBoostClassifier memiliki perbedaan nilai akurasi terkecil, hanya selisih 0.4%. Meskipun AdaBoostClassifier memiliki perbedaan nilai terkecil, tetapi untuk nilai akurasi pada data training dan testing lebih kecil daripada model yang lain. DecisionTreeClassifier memiliki nilai akurasi yang sangat tinggi pada data training, tetapi memiliki nilai akurasi yang cukup kecil pada data testing dengan perbedaan mencapai 20%. Bisa dikatakan bahwa DecisionTreeClassifier mengalami overfitting.
# %% [markdown]
# ### Cross Validation for Some Metrics
# %% [markdown]
# Kali ini kita akan lakukan cross validation untuk mengukur performa model dengan beberapa metrik, yaitu accuracy, precision, recall, dan f1-score.

# %%
skfold = StratifiedKFold(n_splits=5, random_state=42, shuffle=True)

# Cross validation for each model
dtc_score = cross_validate(models[0], X, y, scoring=('accuracy', 'precision', 'recall', 'f1'), cv=skfold, n_jobs=-1, verbose=1)
rfc_score = cross_validate(models[1], X, y, scoring=('accuracy', 'precision', 'recall', 'f1'), cv=skfold, n_jobs=-1, verbose=1)
abc_score = cross_validate(models[2], X, y, scoring=('accuracy', 'precision', 'recall', 'f1'), cv=skfold, n_jobs=-1, verbose=1)
etc_score = cross_validate(models[3], X, y, scoring=('accuracy', 'precision', 'recall', 'f1'), cv=skfold, n_jobs=-1, verbose=1)
gbc_score = cross_validate(models[4], X, y, scoring=('accuracy', 'precision', 'recall', 'f1'), cv=skfold, n_jobs=-1, verbose=1)
bgc_score = cross_validate(models[5], X, y, scoring=('accuracy', 'precision', 'recall', 'f1'), cv=skfold, n_jobs=-1, verbose=1)
knn_score = cross_validate(models[6], X, y, scoring=('accuracy', 'precision', 'recall', 'f1'), cv=skfold, n_jobs=-1, verbose=1)
logreg_score = cross_validate(models[7], X, y, scoring=('accuracy', 'precision', 'recall', 'f1'), cv=skfold, n_jobs=-1, verbose=1)
nb_score = cross_validate(models[8], X, y, scoring=('accuracy', 'precision', 'recall', 'f1'), cv=skfold, n_jobs=-1, verbose=1)
svm_score = cross_validate(models[9], X, y, scoring=('accuracy', 'precision', 'recall', 'f1'), cv=skfold, n_jobs=-1, verbose=1)
xgb_score = cross_validate(models[10], X, y, scoring=('accuracy', 'precision', 'recall', 'f1'), cv=skfold, n_jobs=-1, verbose=1)
mlp_score = cross_validate(models[11], X, y, scoring=('accuracy', 'precision', 'recall', 'f1'), cv=skfold, n_jobs=-1, verbose=1)


# %%
cv_result = [
    dtc_score, rfc_score, abc_score, etc_score, gbc_score, bgc_score, 
    knn_score, logreg_score, nb_score, svm_score, xgb_score, mlp_score]

# Average score for each metrics
df_cv_result = pd.DataFrame(cv_result, index=model_name).applymap(np.mean)
df_cv_result = df_cv_result.sort_values(['test_accuracy', 'test_recall'], ascending=False)
df_cv_result = df_cv_result.reset_index()
df_cv_result.rename(columns={'index':'Model'}, inplace=True)
df_cv_result

# %% [markdown]
# Dari hasil diatas, GradientBoostingClassifier memiliki nilai akurasi dan dan recall yang paling tinggi dari keseluruhan model. Selain nilai akurasi, recall juga akan kita perhitungkan karena **kita lebih ingin model kita dapat mengklasifikasi lebih banyak False Positive(FP) daripada False Negative (FN)**. 
# FP pada kasus ini yaitu model memprediksi prospek akan dikonversi, tetapi sebenarnya tidak dikonversi. Maka FP lebih baik daripada FN. FN yaitu model memprediksi prospek tidak akan di konversi tetapi sebenarnya dapat dikonversi, dan hal ini dapat menyebabkan semakin banyak prospek yang tidak jadi dikonversi.  
# 
# > Dari keseluruhan proses diatas, maka saya akan memilih model **GradientBoostingClassifier** karena memiliki nilai akurasi dan recall yang tertinggi. Meskipun perbedaan akurasi nya lebih besar dari AdaBoostClassifier, tetapi AdaBoostClassifier tidak cukup besar pada nilai akurasi dan recall daripada GradientBoostingClassifier.
# %% [markdown]
# ## Gradient Boosting Classifier
# %% [markdown]
# ### Default Parameter

# %%
gbc = GradientBoostingClassifier()
gbc.fit(X_train_over, y_train_over)

y_pred = gbc.predict(X_test)

train_score_def = round((gbc.score(X_train_over, y_train_over) * 100), 2)
test_score_def = round((gbc.score(X_test, y_test) * 100), 2)
prec_score_def = round((precision_score(y_test, y_pred)) * 100, 2)
recall_score_def = round((recall_score(y_test, y_pred)) * 100, 2)

print('Training Accuracy : {}%'.format(train_score_def))
print('Test Accuracy : {}%'.format(test_score_def))
print('Precision Score : {}%'.format(prec_score_def))
print('Recall Score : {}%'.format(recall_score_def))

# %% [markdown]
# ### Tuning Hyperparameters

# %%
gbc = GradientBoostingClassifier()

# define parameters
params = {
    # 'loss':['deviance', 'exponential'],
    'n_estimators':range(100, 226, 25),
    # 'criterion':['friedman_mse', 'squared_error', 'mse', 'mae'],
    'max_depth':range(0, 31, 5),
    'max_features':['auto', 'sqrt', 'log2']
}

grid_result = GridSearchCV(gbc, params, scoring='accuracy', cv=5)


# %%
# Fitting grid search
grid_result.fit(X_train_over, y_train_over)


# %%
grid_result.best_params_


# %%
gbc_tuned = GradientBoostingClassifier(**grid_result.best_params_)
gbc_tuned.fit(X_train_over, y_train_over)

y_pred_tuned = gbc_tuned.predict(X_test)

train_score_tuned = round((gbc_tuned.score(X_train_over, y_train_over) * 100), 2)
test_score_tuned = round((gbc_tuned.score(X_test, y_test) * 100), 2)
prec_score_tuned = round((precision_score(y_test, y_pred_tuned)) * 100, 2)
recall_score_tuned = round((recall_score(y_test, y_pred_tuned)) * 100, 2)

print('Training Accuracy : {}%'.format(train_score_tuned))
print('Test Accuracy : {}%'.format(test_score_tuned))
print('Precision Score : {}%'.format(prec_score_tuned))
print('Recall Score : {}%'.format(recall_score_tuned))


# %%
pd.DataFrame({
    'train_acc':[train_score_def, train_score_tuned],
    'test_acc':[test_score_def, test_score_tuned],
    'precision':[prec_score_def, prec_score_tuned],
    'recall':[recall_score_def, recall_score_tuned]}, index=['gbc_default', 'gbc_tuned'])

# %% [markdown]
# Pada hasil diatas dapat dilihat hasil training menggunakan default parameter dan hyperparameter tuning. Dari hasil training menggunakan hyperparameter tuning, model dapat memperoleh akurasi mencapai sekitar 91.80% pada data training, tetapi menurun menjadi sekitar 81.27% pada data testing. Pada training menggunakan default parameter, model menghasilkan akurasi sekitar 84.24% pada data training dan 82.70% pada data testing. GradientBoosting dengan menggunakan default parameter menghasilkan nilai recall lebih kecil daripada pada GradientBoosting hasil hyperparameter tuning dengan perbedaan sekitar 1%.
# 
# > Dari hasil diatas, hyperparameter tuning meningkatkan akurasi dan recall pada data training dan menurunkan nilai akurasi pada data testing. Maka dapat dikatakan bahwa bahwa model mengalami sedikit overfitting. Maka pada training model ini **saya akan memilih model GradientBoostingClassifier dengan default parameter** karena perbedaan akurasi pada data training dan testing tidak terlalu jauh. Meskipun nilai recall nya lebih kecil dari pada model hasil hyperparameter tuning,tetapi perbedaannya tidak terlalu jauh.
# %% [markdown]
# # Model Evaluation
# %% [markdown]
# ## Confusion Matrix

# %%
# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
ConfusionMatrixDisplay(cm).plot()
plt.show()

# %% [markdown]
# Pada confusion matrix diatas, model dapat mengklasifikasi class 0 (Not Converted) dengan benar sebanyak 966 data dan mengklasifikasi class 1 (Converted) sebanyak 534 data.
# %% [markdown]
# ## Classification Report

# %%
# Classification report model
cr = classification_report(y_test, y_pred)
print(cr)

# %% [markdown]
# Dari hasil classification report diatas, model memperoleh akurasi sebesar 83%.
# %% [markdown]
# ## Precision Recall and ROC Curve

# %%
# Precision Recall Curve
y_pred = gbc.decision_function(X_test)
prec, recall, _ = precision_recall_curve(y_test, y_pred, pos_label=gbc.classes_[1])
pr_display = PrecisionRecallDisplay(prec, recall)


# %%
# ROC Curve
fpr, tpr, _ = roc_curve(y_test, y_pred, pos_label=gbc.classes_[1])
roc_display = RocCurveDisplay(fpr=fpr, tpr=tpr)


# %%
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

pr_display.plot(ax=ax1)
roc_display.plot(ax=ax2)
ax1.set_title('Precision Recall Curve')
ax2.set_title('ROC Curve')
plt.show()

# %% [markdown]
# ## Feature Importance

# %%
# Create dataframe for store feature importance score
feature_importance = pd.DataFrame(
    gbc.feature_importances_, 
    index = X.columns,
    columns=['importance']
).sort_values('importance', ascending=False)

print(feature_importance)

# Plotting feature importance
plt.figure(figsize=(15, 10))
sns.barplot(data=feature_importance, x='importance', y=feature_importance.index, color='blue')
plt.title('Feature Importance', fontsize=20, color='black', pad=15)
plt.show()

# %% [markdown]
# Pada visualisasi diatas, dapat dilihat bahwa feature Total Time Spent On Website merupakan feature yang paling penting dengan nilai 0.32. Feature Last Origin_Lead Add Form dan Last Acttivity_SMS Sent feature kedua dan ketiga yang paling penting dengan nilai masing-masing 0.18 dan 0.13  
# %% [markdown]
# ## Thresholds Adjustment

# %%
# Prdiction probability
y_pred = gbc.predict_proba(X_test)[:, 1]

fpr, tpr, thresholds = roc_curve(y_test, y_pred)
roc_auc = auc(fpr, tpr)
print(f'Area Under the ROC Curve {roc_auc}')

####################################
# The optimal cut off would be where tpr is high and fpr is low
# tpr - (1-fpr) is zero or near to zero is the optimal cut off point
####################################

i = np.arange(len(tpr)) # index for df
roc = pd.DataFrame({
    'fpr':pd.Series(fpr, index=i),
    'tpr':pd.Series(tpr, index=i),
    '1-fpr':pd.Series(1-fpr, index = i),
    'tf' : pd.Series(tpr - (1-fpr), index = i), 
    'thresholds' : pd.Series(thresholds, index = i)
})
roc.iloc[(roc.tf-0).abs().argsort()[:1]]


# %%
# Plot tpr vs 1-fpr
plt.figure(figsize=(8, 5))
plt.plot(roc['tpr'])
plt.plot(roc['1-fpr'], color = 'red')
plt.xlabel('1-False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic', fontsize=20, color='black', pad=15)
plt.savefig('Receiver operating characteristic', dpi=600)
plt.show()

# %% [markdown]
# Dari hasil diatas didapatkan thresholds paling ideal, yaitu 0.440399.  
# Maka setelah didapatkan thresholds yang optimal, maka thresholds tersebut kita gunakan untuk klasifikasi.
# - Jika lebih dari nilai tersebut maka termasuk "Hot Lead"
# - JIka sebaliknya berarti "Cold Lead".

# %%
# Create dataframe for apppying thresholds
y_pred_final = pd.DataFrame({'Converted':y_test.values, 'Converted_Prob':y_pred})
y_pred_final['final_prediction'] = y_pred_final['Converted_Prob'].apply(lambda x: 1 if x > 0.440399 else 0)
y_pred_final.head(10)

# %% [markdown]
# ### Confusion Matrix

# %%
# Confusion Matrix
cm = confusion_matrix(y_pred_final['Converted'], y_pred_final['final_prediction'])
print(cm)
# Plotting confusion matrix
ConfusionMatrixDisplay(cm, display_labels=gbc.classes_).plot()
plt.show()

# %% [markdown]
# Dari hasil thresholds adjusment dapat dilihat bahwa hasilnya terdapat 927 berhasil diklasifikasi sebagai class 0 (Not Converted) dan sebanyak 559 diklasifikasi sebagai class 1 (Converted).
# %% [markdown]
# ### Classification Report 

# %%
# Classification Report 
cr = classification_report(y_pred_final['Converted'], y_pred_final['final_prediction'])
print(cr)

# %% [markdown]
# Dari hasil Precision Recall Cut-Off point, output dari model terlihat mengalami perbedaan : <br>
# **Tanpa Precision Recall Trade-Off** : 
# - TP (539)
# - TN (962)
# - FP (163)
# - FN (151) <br>
# 
# Accuracy = 82.64% <br>
# Precision = 76.67% <br>
# Recall = 78.11%
# 
# **Dengan Precision Recall Trade-Off** :
# - TP (559)
# - TN (927)
# - FP (198)
# - FN (131)
# 
# Accuracy = 81.87% <br>
# Precision = 73.84% <br>
# Recall = 81.01%
# 
# Pada tujuan awal kita, CEO ingin mengidentifikasi prospek yang akan dikonversi. Karena menggunakan nilai thresholds menyebabkan TP berkurang dan False Positive meningkat dan hal tersebut memperbesar nilai recall, maka kita akan menggunakan thresholds.
# %% [markdown]
# # Save Model

# %%
filename = 'final_model.sav'
import pickle
pickle.dump(gbc, open(filename, 'wb'))


