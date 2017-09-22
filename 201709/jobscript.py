gen_jar   = 'W2C'
classpath = '../201705/PythonWithWeka'
gen_pyw2c_path = '../201705/PythonWithWeka/getPyW2CMd.py'
import os
os.system("""
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64
export CLASSPATH=.:$JAVA_HOME/lib:$JAVA_HOME/jre/lib:$CLASSPATH  
export PATH=$JAVA_HOME/bin:$JAVA_HOME/jre/bin:$PATH 
""")
weka_source = './weka'
train = lambda weka_source : lambda feature_trans_model_to_save:\
        lambda min_count: lambda max_count: lambda WekaResults:\
	    os.system(f"java -Xmn512m -Xms1024m -Xmx10000m  -Djava.ext.dirs={classpath}/lib -cp {classpath} {gen_jar} train {weka_source} {feature_trans_model_to_save} {min_count} {max_count} {WekaResults}")

toPyModel = lambda weka_source: lambda WekaResults : lambda pathForPyModel: os.system(f"python {gen_pyw2c_path} {weka_source} {WekaResults} {pathForPyModel}" )
for count in (None, 1, 2, 3):
    print(count)
    if count is None:
        count = "mix"
        min_count = 1
        max_count = 3
    else:
        min_count = max_count = count
    feature_trans_model_to_save = f"javaObj-gram-{count}"
    WekaResults                 = f"javaWekaMd-gram-{count}"
    pathForPyModel              = f"Models/pythonMd-gram-{count}.json"
    train(weka_source)(feature_trans_model_to_save)(min_count)(max_count)(WekaResults)
    toPyModel(weka_source)(WekaResults)(pathForPyModel)





