import numpy as np
import pandas as pd
import argparse
import pickle
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import mutual_info_classif
from sklearn.feature_selection import SelectKBest
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, recall_score, precision_score, f1_score, roc_auc_score

class Trainer:
    def __init__(self, train_path, save_path):
        self.train_path = train_path
        self.model = RandomForestClassifier(random_state = 42)
        self.preprocessor = StandardScaler()
        self.label_encoder = preprocessing.LabelEncoder()
        self.save_path = save_path

    def load_dataset(self):
        # Vi bo du lieu ban dau khong co ten cot nen can dat ten cot cho dataframe
        columns = (['duration','protocol_type','service','flag'
            ,'src_bytes','dst_bytes','land','wrong_fragment','urgent'
            ,'hot','num_failed_logins','logged_in','num_compromised'
            ,'root_shell','su_attempted','num_root','num_file_creations'
            ,'num_shells','num_access_files','num_outbound_cmds'
            ,'is_host_login','is_guest_login','count','srv_count','serror_rate'
            ,'srv_serror_rate','rerror_rate','srv_rerror_rate','same_srv_rate'
            ,'diff_srv_rate','srv_diff_host_rate','dst_host_count','dst_host_srv_count'
            ,'dst_host_same_srv_rate','dst_host_diff_srv_rate','dst_host_same_src_port_rate'
            ,'dst_host_srv_diff_host_rate','dst_host_serror_rate','dst_host_srv_serror_rate'
            ,'dst_host_rerror_rate','dst_host_srv_rerror_rate','attack','level'])
        self.df_train = pd.read_csv(self.train_path)
        self.df_train.columns = columns

    def categorical_attack_type(self):
        # Chia attack label thanh 3 lop normal, ddos, unauthorized_access
        dos_attacks = ['apache2','back','land','neptune','mailbomb','pod','processtable','smurf','teardrop','udpstorm','worm']
        unauthorized_Access = ['ftp_write','guess_passwd','http_tunnel','imap','multihop','named','phf','sendmail','snmpgetattack','snmpguess','spy','warezclient','warezmaster','xclock','xsnoop'
                       'ipsweep','mscan','nmap','portsweep','saint','satan',
                       'buffer_overflow','loadmodule','perl','ps','rootkit','sqlattack','xterm']
        
        attack_n = []
        for i in self.df_train.attack:
            if i == 'normal':
                attack_n.append("normal")
            elif i in dos_attacks:
                attack_n.append("ddos")
            else:
                attack_n.append("unauthorized_access")
        self.df_train['attack'] = attack_n

    def preprocessing(self):
        clm = ['protocol_type', 'service', 'flag', 'attack']
        for x in clm:
            self.df_train[x] = self.label_encoder.fit_transform(self.df_train[x])
    
    def evaluate(self, X_train, y_train, X_test, y_test):
        #it's a helper function in order to evaluate our model if it's overfit or underfit.

        y_train_pred = self.model.predict(X_train)
        y_pred = self.model.predict(X_test)
        
        print("Test_Set")
        print(confusion_matrix(y_test, y_pred))
        print(classification_report(y_test, y_pred))
        print()
        print("Train_Set")
        print(confusion_matrix(y_train, y_train_pred))
        print(classification_report(y_train, y_train_pred))

    def save_weight(self):
        # Save the model
        with open(self.save_path, 'wb') as f:
            pickle.dump({'preprocessor': self.preprocessor, 'model': self.model, "label_encoder": self.label_encoder}, f)

    def train(self):
        self.load_dataset()
        # Train test split
        clm = ['protocol_type', 'service', 'flag', 'attack']
        for x in clm:
            self.df_train[x] = self.label_encoder.fit_transform(self.df_train[x])
        X = self.df_train.drop(["attack"], axis=1)
        y = self.df_train["attack"]
        X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.2,random_state=43)

        # Feature selection
        columns=['duration', 'protocol_type', 'service', 'flag', 'src_bytes',
        'dst_bytes', 'wrong_fragment', 'hot', 'logged_in', 'num_compromised',
        'count', 'srv_count', 'serror_rate', 'srv_serror_rate', 'rerror_rate']
        X_train=X_train[columns]
        X_test=X_test[columns]

        # scale
        X_train = self.preprocessor.fit_transform(X_train)
        X_test = self.preprocessor.transform(X_test) # we use only transform in order to prevent data leakage

        self.model.fit(X_train,y_train)
        self.evaluate(X_train, y_train, X_test, y_test)
        self.save_weight()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train_path", type=str, required=True, help="Path to csv path for training data")
    parser.add_argument("--save_path", type=str, required=True, help="Path to save trained model")
    args = parser.parse_args()
    trainer = Trainer(train_path=args.train_path, save_path=args.save_path)
    trainer.train()