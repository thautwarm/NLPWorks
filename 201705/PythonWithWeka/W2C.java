import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import weka.core.Instances;
import weka.core.converters.TextDirectoryLoader;
import weka.core.tokenizers.NGramTokenizer;
import weka.filters.Filter;	
import weka.filters.unsupervised.attribute.StringToWordVector;

public class W2C {
	public static void main(String[] args) throws Exception {

		//  args[0]: train
		//         args[1]: input-file-name of training datas.
		//         args[2]: output-file-name of the feature-transforming model.
 		//         args[3]: min of the grams.
		//         args[4]: max of the grams.
		//         args[5]: the outfile-name of the results about dealing with the training datas.
		//             If the value is "pass", the results will not be saved. 
				if (args[0].equals("train")){
				lin(args);
			}
			else{
			in(args);	
			}
		  
		  }
    public static void lin(String[] args) throws Exception {
	    TextDirectoryLoader loader = new TextDirectoryLoader();
	    loader.setDirectory(new File(args[1]));
	    Instances dataRaw = loader.getDataSet();
	    NGramTokenizer tokenizer=new NGramTokenizer();
	    tokenizer.setNGramMinSize(Integer.parseInt( args[3] ));
	    tokenizer.setNGramMaxSize(Integer.parseInt( args[4] ));
	    StringToWordVector filter = new StringToWordVector();
	    filter.setTokenizer(tokenizer);
	    filter.setInputFormat(dataRaw);
	    filter.setTFTransform(true); 
	    filter.setIDFTransform(true); 
	    filter.setWordsToKeep(1000000); 
	    filter.setMinTermFreq(5); 
	    Instances dataFiltered=Filter.useFilter(dataRaw, filter);
	    ObjectOutputStream oos=new ObjectOutputStream(new FileOutputStream(args[2]));
	    oos.writeObject(filter);
	    oos.flush();
	    oos.close();
	    if (args[5].equals("pass"))
	    {
	    	return;
	    }
	   	File writename = new File(args[5]);
	    BufferedWriter fileout = new BufferedWriter(new FileWriter(writename));
	    fileout.write(dataFiltered.toString());
	    fileout.flush();fileout.close();
	   
    }
    public static void in(String[] args)throws Exception{
    	ObjectInputStream ios = new ObjectInputStream(new FileInputStream(args[1]));
    	StringToWordVector md = (StringToWordVector) ios.readObject();;
    	TextDirectoryLoader t = new TextDirectoryLoader();
    	t.setDirectory(new File(args[2]));
    	Instances dataRaw = t.getDataSet();
    	Instances dataFiltered = Filter.useFilter(dataRaw, md);
	    ios.close();
	    File writename = new File(args[3]);
	    BufferedWriter fileout = new BufferedWriter(new FileWriter(writename));
	    fileout.write(dataFiltered.toString());
	    fileout.flush();fileout.close();
    }
}
