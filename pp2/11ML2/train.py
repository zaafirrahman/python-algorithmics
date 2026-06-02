import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, accuracy_score

# Step 1. Loading and cleaning data
df = pd.read_csv('train.csv')

kolom_object = df.select_dtypes(include=['object']).columns

df = df.drop(columns=['career_start', 'career_end', 'last_seen', 'occupation_name', 'bdate'])

df['langs'] = df['langs'].apply(lambda x: 1 if x == 'False' or pd.isna(x) else len(str(x).split(';')))


# 1. Isi NaN dengan 'Unknown' terlebih dahulu
df['city'] = df['city'].fillna('Unknown')
# 2. Ambil list 10 kota terbanyak (termasuk 'Unknown' jika dia masuk top 10)
top_10_cities = df['city'].value_counts().head(10).index
# 3. Kelompokkan sisanya menjadi 'Other'
df['city'] = df['city'].apply(lambda x: x if x in top_10_cities else 'Other')

# One-Hot Encoding untuk kolom city, otomatis nge-drop kolom teks aslinya
df = pd.get_dummies(df, columns=['city'], dtype=int)

kolom_object = df.select_dtypes(include=['object']).columns

edu_mapping = {
    'Undergraduate applicant': 0,
    'Student (Bachelor\'s)': 1,
    'Alumnus (Bachelor\'s)': 2,
    'Student (Specialist)': 3,
    'Alumnus (Specialist)': 4,
    'Student (Master\'s)': 5,
    'Alumnus (Master\'s)': 6,
    'Candidate of Sciences': 7,
    'PhD': 8
}

df['education_status_encoded'] = df['education_status'].map(edu_mapping)
df = df.drop(columns=['education_status'])

# Ubah string/boolean 'False' atau NaN menjadi kode angka -1
df['life_main'] = df['life_main'].replace({'False': -1, False: -1}).fillna(-1).astype(int)
df['people_main'] = df['people_main'].replace({'False': -1, False: -1}).fillna(-1).astype(int)

# Karena ini kode kategori acak, pecah pake One-Hot Encoding biar KNN gak bingung
df = pd.get_dummies(df, columns=['life_main', 'people_main'], dtype=int, prefix=['life', 'people'])

# Isi data kosong dengan 'Unknown'
df['education_form'] = df['education_form'].fillna('Unknown')
df['occupation_type'] = df['occupation_type'].fillna('Unknown')

# One-Hot Encoding barengan!
df = pd.get_dummies(df, columns=['education_form', 'occupation_type'], dtype=int)

# 1. Pisahkan Fitur (X) dan Target (y)
# Jangan lupa drop 'id' karena nomor urut tidak punya korelasi jarak geometris
X = df.drop(columns=['result', 'id'], errors='ignore')
y = df['result']

# 2. Split Data (75% Training, 25% Testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

# 3. Eksekusi Standardisasi (Z-score Scaling)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 4. Inisialisasi dan Train Model KNN
# Kita set n_neighbors=5 sebagai baseline awal
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train_scaled, y_train)

# 5. Prediksi dan Cek Performa
y_pred = knn.predict(X_test_scaled)

print('Accuracy:', accuracy_score(y_test, y_pred) * 100)
print('Confusion matrix:')
print(confusion_matrix(y_test, y_pred))