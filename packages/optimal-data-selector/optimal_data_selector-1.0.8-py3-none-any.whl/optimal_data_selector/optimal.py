def optimal_data_selector(predictor,target,combination=10,random_state=0,train_size=0.7,bs_problem='class',time_forecast=True,scaling=None,acc_forecast=True,boost=None,randomness=True):
    '''Find the best data combination for models by maximizing accuracy on different sizes of data.

    Parameters:
        predictor     : array-like
            The independent variables used for prediction.
            
        target        : array-like
            The target variable to be predicted.
            
        combination   : int, optional
            The number of combinations of data to consider. Default is 10.
            
        random_state  : int, optional
            The seed value for random number generation. Default is 0.
            
        train_size    : float, optional
            The proportion of data used for training. Default is 0.7.
            
        bs_problem    : str, optional --> ['reg','class']
            The type of problem to solve. Options are 'class' for classification problems and 'reg' for regression problems.
            Default is 'class'.
            
        time_forecast : bool, optional --> [True,False]
            Flag indicating whether to print the computation time. Default is True.
            
        scaling       : str, optional --> ['normal','st_normal']
            it takes the data and scale the value based on the option you have choosed, options are ['normal','st_normal'].Default is None
            
        boost         : str, optional --> [None,'prim','max']
            Flag indicating whether to use boosting performance or reduce the time complexcity [None,'prim','max']. 
             When None, the function will try to find fully stabel data combination this case the function gives
             Completely zero weightage to  time saving , When 'prim', the function will look towards balanced data as well as
             less time this case function will give 50:50 weightage to both , When 'max', In this case time saving
             will be the first priority . Default is None.
             
        randomness    : bool, True --> [True,False]
            it takes the mixture to the data combo from data, turn it into False to have sequential data 
                    
    Returns:
        x_train : array-like
            The training data for the independent variables.
        x_test  : array-like
            The testing data for the independent variables.
        y_train : array-like
            The training data for the target variable.
        y_test  : array-like
            The testing data for the target variable.

    Notes:
        - For classification problems ('bs_problem' = 'class').
        - For regression problems ('bs_problem' = 'reg'), the function gives the best data to make a perfect model.
        - The function calculates the accuracy of each model on different data combinations and returns the combination
          with the highest accuracy.
        - If 'time_forecast' is set to True, the function prints the computation time in minutes.
        - If 'scaling' value is given among the options ,it scales the data and perfomes the actions on it 
        - If boost is set to True, only a single model will be used in (classification) or (regression).
          In the case of  False, multiple models are considered.
          
        *** Make sure that you are giving less number of combinations, if your data  is very large in size. 
        *** If the boost is set on None then function will take more time to give the result but the data will be 
            too stabel as compair to other values , but If it's set on the False then it will take very less time 
            {this parameter has advantage and disadvantage as well}
        *** The values of boost perameter:
        
                                         Stability of data combo  |      Time saving 
                                         _________________________|_______________________
                                         None > 'prim' > 'max'    | 'max' > 'prim' > None
                                                                  |

    Examples:
        # Classification problem
        x_train, x_test, y_train, y_test = optimal_data_selector(predictor, target, combination=5, random_state=42,
                                                              train_size=0.8, bs_problem='class',scaling='normal',boost='max',randomness=False)

        # Regression problem
        x_train, x_test, y_train, y_test = optimal_data_selector(predictor, target, combination=10, random_state=0,
                                                              train_size=0.7, bs_problem='reg',scaling='st_normal',boost='prim',randomness=True)
    '''
    try:
        X=predictor
        Y=target
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import MinMaxScaler,StandardScaler
        from sklearn.linear_model import LogisticRegression,LinearRegression,Ridge
        from sklearn.svm import SVC
        from sklearn.tree import DecisionTreeClassifier,DecisionTreeRegressor
        from sklearn.naive_bayes import GaussianNB,MultinomialNB
        import scipy
        import time
        import warnings
        warnings.filterwarnings('ignore')
        if scaling == 'normal':
            minmax=MinMaxScaler()
            X=minmax.fit_transform(X)
        elif scaling == 'st_normal':
            std=StandardScaler()
            X=std.fit_transform(X)
        x_train=[]
        x_train1=[]
        avg=[]
        acc=[]
        avg_acc=[]
        i3=[]
        i4=[]
        a=0
        chunk=0
        if boost == 'max':
            if bs_problem =='class':
                start0 = time.time()
                for i in range(random_state,random_state+combination):
                    x_train1,x_test1,y_train1,y_test1=train_test_split(X,Y,train_size=train_size,random_state=i,shuffle=randomness)
                    x_train.append([x_train1,y_train1,x_test1,y_test1])
                for x in x_train:
                    log1=LogisticRegression()
                    log1.fit(x[0],x[1])
                    acc.append(log1.score(x[2],x[3]))  
                    a=acc.index(max(acc))
                x_train1=x_train[a][0]
                x_test1=x_train[a][2]
                y_train1=x_train[a][1]
                y_test1=x_train[a][3]
                end0=time.time()
                if acc_forecast == True:
                    print('Accuracy can be ~ '+str(max(acc)))
                if time_forecast == True:
                    print('Computation time = '+str((end0-start0)/60),' mints')     
                return x_train1,x_test1,y_train1,y_test1
            elif bs_problem =='reg':
                start01 = time.time()
                for i in range(random_state,random_state+combination):
                    x_train1,x_test1,y_train1,y_test1=train_test_split(X,Y,train_size=train_size,random_state=i,shuffle=randomness)
                    x_train.append([x_train1,y_train1,x_test1,y_test1])
                for x in x_train:
                    lin=LinearRegression()
                    lin.fit(x[0],x[1])
                    acc.append(lin.score(x[2],x[3]))  
                    a=acc.index(max(acc))
                x_train1=x_train[a][0]
                x_test1=x_train[a][2]
                y_train1=x_train[a][1]
                y_test1=x_train[a][3]
                end01=time.time()
                if acc_forecast == True:
                    print('Accuracy can be ~ '+str(max(acc)))
                if time_forecast == True:
                    print('Computation time = '+str((end01-start01)/60),' mints')    
                return x_train1,x_test1,y_train1,y_test1
        
        elif bs_problem == 'class' and boost == None and type(predictor) != scipy.sparse._csr.csr_matrix:
            start = time.time()
            for i in range(random_state,random_state+combination):
                x_train1,x_test1,y_train1,y_test1=train_test_split(X,Y,train_size=train_size,random_state=i,shuffle=randomness)
                x_train.append([x_train1,y_train1,x_test1,y_test1])
                log=LogisticRegression()
                svm=SVC()
                dis=DecisionTreeClassifier(random_state=random_state)
                nb=GaussianNB()
                clas=[log,svm,nb,dis]
            for x in x_train:
                for c in clas:
                    c.fit(x[0],x[1])
                    acc.append(c.score(x[2],x[3]))  
            for i in range(0, len(acc), 4):
                chunk = acc[i:i+4]
                i3.append(chunk)
            for i in i3:
                i4.append(sum(i)/len(i))
                a=i4.index(max(i4))
            x_train1=x_train[a][0]
            x_test1=x_train[a][2]
            y_train1=x_train[a][1]
            y_test1=x_train[a][3]
            end=time.time()
            if acc_forecast == True:
                print('Accuracy can be ~ '+str(max(i4)))
            if time_forecast == True:
                print('Computation time = '+str((end-start)/60),' mints')
            return x_train1,x_test1,y_train1,y_test1
        elif bs_problem == 'class' and boost == None and type(predictor) == scipy.sparse._csr.csr_matrix:
            
            start22 = time.time()
            for i in range(random_state,random_state+combination):
                x_train1,x_test1,y_train1,y_test1=train_test_split(X,Y,train_size=train_size,random_state=i,shuffle=randomness)
                x_train.append([x_train1,y_train1,x_test1,y_test1])
                log=LogisticRegression()
                svm=SVC()
                dis=DecisionTreeClassifier(random_state=random_state)
                nb2=MultinomialNB()
                clas=[log,svm,nb2,dis]
            for x in x_train:
                for c in clas:
                    c.fit(x[0],x[1])
                    acc.append(c.score(x[2],x[3]))  
            for i in range(0, len(acc), 4):
                chunk = acc[i:i+4]
                i3.append(chunk)
            for i in i3:
                i4.append(sum(i)/len(i))
                a=i4.index(max(i4))
            x_train1=x_train[a][0]
            x_test1=x_train[a][2]
            y_train1=x_train[a][1]
            y_test1=x_train[a][3]
            end22=time.time()
            if acc_forecast == True:
                print('Accuracy can be ~ '+str(max(i4)))
            if time_forecast == True:
                print('Computation time = '+str((end22-start22)/60),' mints')
            return x_train1,x_test1,y_train1,y_test1
                
        elif bs_problem == 'reg' and boost == None:
            start1=time.time()
            for i in range(random_state,random_state+combination):
                x_train1,x_test1,y_train1,y_test1=train_test_split(X,Y,train_size=train_size,random_state=i,shuffle=randomness)
                x_train.append([x_train1,y_train1,x_test1,y_test1])
                lin=LinearRegression()
                rid=Ridge()
                dis1=DecisionTreeRegressor(random_state=random_state)
                rig=[lin,rid,dis1]
            for x in x_train:
                for c in rig:
                    c.fit(x[0],x[1])
                    acc.append(c.score(x[2],x[3]))
            for i in range(0, len(acc), 3):
                chunk = acc[i:i+3]
                i3.append(chunk)
            for i in i3:
                i4.append(sum(i)/len(i))
                a=i4.index(max(i4))
            x_train1=x_train[a][0]
            x_test1=x_train[a][2]
            y_train1=x_train[a][1]
            y_test1=x_train[a][3]
            end1=time.time()
            if acc_forecast == True:
                print('Accuracy can be ~ '+str(max(i4)))
            if time_forecast == True:
                print('Computation time = '+str((end1-start1)/60),' mints')
            return x_train1,x_test1,y_train1,y_test1
        
        elif bs_problem == 'class' and boost == 'prim' and type(predictor) == scipy.sparse._csr.csr_matrix:
            start9 = time.time()
            for i in range(random_state,random_state+combination):
                x_train1,x_test1,y_train1,y_test1=train_test_split(X,Y,train_size=train_size,random_state=i,shuffle=randomness)
                x_train.append([x_train1,y_train1,x_test1,y_test1])
                log=LogisticRegression()
                nb=MultinomialNB()
                clas=[log,nb]
            for x in x_train:
                for c in clas:
                    c.fit(x[0],x[1])
                    acc.append(c.score(x[2],x[3]))  
            for i in range(0, len(acc), 2):
                chunk = acc[i:i+2]
                i3.append(chunk)
            for i in i3:
                i4.append(sum(i)/len(i))
                a=i4.index(max(i4))
            x_train1=x_train[a][0]
            x_test1=x_train[a][2]
            y_train1=x_train[a][1]
            y_test1=x_train[a][3]
            end9=time.time()
            if acc_forecast == True:
                print('Accuracy can be ~ '+str(max(i4)))
            if time_forecast == True:
                print('Computation time = '+str((end9-start9)/60),' mints')
            return x_train1,x_test1,y_train1,y_test1
        
        elif bs_problem == 'class' and boost == 'prim' and type(predictor) != scipy.sparse._csr.csr_matrix:
            start10 = time.time()
            for i in range(random_state,random_state+combination):
                x_train1,x_test1,y_train1,y_test1=train_test_split(X,Y,train_size=train_size,random_state=i,shuffle=randomness)
                x_train.append([x_train1,y_train1,x_test1,y_test1])
                log2=LogisticRegression()
                nb2=GaussianNB()
                clas=[log2,nb2]
            for x in x_train:
                for c in clas:
                    c.fit(x[0],x[1])
                    acc.append(c.score(x[2],x[3]))  
            for i in range(0, len(acc), 2):
                chunk = acc[i:i+2]
                i3.append(chunk)
            for i in i3:
                i4.append(sum(i)/len(i))
                a=i4.index(max(i4))
            x_train1=x_train[a][0]
            x_test1=x_train[a][2]
            y_train1=x_train[a][1]
            y_test1=x_train[a][3]
            end10=time.time()
            if acc_forecast == True:
                print('Accuracy can be ~ '+str(max(i4)))
            if time_forecast == True:
                print('Computation time = '+str((end10-start10)/60),' mints')
            return x_train1,x_test1,y_train1,y_test1
        
        elif bs_problem == 'reg' and boost == 'prim' and type(predictor) != scipy.sparse._csr.csr_matrix:
            start10 = time.time()
            for i in range(random_state,random_state+combination):
                x_train1,x_test1,y_train1,y_test1=train_test_split(X,Y,train_size=train_size,random_state=i,shuffle=randomness)
                x_train.append([x_train1,y_train1,x_test1,y_test1])
                lin2=LinearRegression()
                reg2=Ridge()
                clas=[lin2,reg2]
            for x in x_train:
                for c in clas:
                    c.fit(x[0],x[1])
                    acc.append(c.score(x[2],x[3]))  
            for i in range(0, len(acc), 2):
                chunk = acc[i:i+2]
                i3.append(chunk)
            for i in i3:
                i4.append(sum(i)/len(i))
                a=i4.index(max(i4))
            x_train1=x_train[a][0]
            x_test1=x_train[a][2]
            y_train1=x_train[a][1]
            y_test1=x_train[a][3]
            end10=time.time()
            if acc_forecast == True:
                print('Accuracy can be ~ '+str(max(i4)))
            if time_forecast == True:
                print('Computation time = '+str((end10-start10)/60),' mints')
            return x_train1,x_test1,y_train1,y_test1
            
        
        elif bs_problem !='class' or bs_problem !='reg':
            print("you have input a wrong value as bs_problem")
            
    except ImportError as ir:
        print('Error : '+str(ir))
    except ValueError as vr:
        print('Error : '+str(vr))
    except TypeError as tr:
        print('Error : '+str(tr))
    except NameError as nr:
        print('Error : '+str(nr))
    except NotImplementedError as npr:
        print('Error : '+str(npr))
    except AttributeError as ar:
        print('Error : '+str(ar))
        
    except Exception as ex:
        print('Error : '+str(ex))