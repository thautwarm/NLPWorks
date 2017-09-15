gen_jar = '../201705/PythonWithWeka/W2C'
import os
weka_source = './WekaData'
train = lambda weka_source : lambda feature_trans_model_to_save:\
        lambda min_count: lambda max_count: lambda WekaResults:\
	    os.system(f"python {gen_jar} train {weka_source} {feature_trans_model_to_save} {min_count} {max_count} {WekaResults}")

for count in (1, 2, 3, None):
    print(count)
    if count is None:
        count = "mix"
        min_count = 1
        max_count = 3
    else:
        min_count = max_count = count
    feature_trans_model_to_save = f"javaObj-gram-{count}"
    WekaResults                 = f"javaWekaMd-gram-{count}"
    train(weka_source)(feature_trans_model_to_save)(min_count)(max_count)(WekaResults)




