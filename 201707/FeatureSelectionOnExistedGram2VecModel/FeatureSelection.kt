package decomposition
import weka.*;
import weka.filters.supervised.attribute.AttributeSelection
import weka.attributeSelection.InfoGainAttributeEval
import weka.attributeSelection.Ranker
import weka.attributeSelection.CorrelationAttributeEval
import weka.attributeSelection.ReliefFAttributeEval
import weka.filters.unsupervised.attribute.*;
import weka.core.*;
import weka.filters.*;
import java.io.*;
import java.io.*;

class function {
	var inst:Instances? = null
	var path :String = ""
	fun useEntropy(toNum:Int){
		System.out.println("\nuse entropy")
		val attrselect = AttributeSelection()
		val ranker = Ranker()
		val eval = InfoGainAttributeEval()
		ranker.setNumToSelect(toNum);
		attrselect.setEvaluator(eval)
		attrselect.setSearch(ranker)
		attrselect.setInputFormat(inst)
		val data = Filter.useFilter(inst, attrselect)
		val ios = File(path+"_entropy")
		ios.writeText(data.toString())
		//println(data)
		
	}
	fun useCorr(toNum:Int){
		System.out.println("\nuse corr")
		val attrselect = AttributeSelection()
		val ranker = Ranker()
		val eval = CorrelationAttributeEval()
		ranker.setNumToSelect(toNum);
		attrselect.setEvaluator(eval)
		attrselect.setSearch(ranker)
		attrselect.setInputFormat(inst)
		val data = Filter.useFilter(inst, attrselect)
		val ios = File(path+"_corr")
		ios.writeText(data.toString())
		//println(data)
	}
	fun useRelief(toNum:Int){
		System.out.println("\nuse relief")
		val attrselect = AttributeSelection()
		val ranker = Ranker()
		val eval = ReliefFAttributeEval()
		ranker.setNumToSelect(toNum);
		attrselect.setEvaluator(eval)
		attrselect.setSearch(ranker)
		attrselect.setInputFormat(inst)
		val data = Filter.useFilter(inst, attrselect)
		val ios = File(path+"_relief")
		ios.writeText(data.toString())
		//println(data)
	}
	fun Go(args:Array<String>){
		
		val filter = NumericToNominal()
		
		val data =   Instances(BufferedReader(FileReader(args[0]) ))
		if (data.classIndex() == -1)
			data.setClassIndex(data.numAttributes() - 1)
		filter.setInputFormat(data)
		path = args[0]
		inst = Filter.useFilter(data, filter)
		val selectNum = args[1].toInt()
		useCorr(selectNum)
		useEntropy(selectNum)
		useRelief(selectNum)
	}
	
}
fun main(args:Array<String>){
	val go = function()
	go.Go(args)
	
}