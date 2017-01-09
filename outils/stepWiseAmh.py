import math
class StepWiseAMH:
    """StepWise implementation"""
    
    all_models=X_validation.columns # All models
    
    #==========================================================#
    def __init__(self,k_best=5,max_models=50,epslon=0.01,random=False):
        self.random=random # if true select k_best random models, else k_best best models in initial step
        self.k_best=k_best # Number of models in the nitial ensemble
        self.max_models=max_models # number maximal of models in ensemble
        self.epslon=epslon # if new_score - old_score is positif and less than epsilon ==> stop
        self.ensemble_models=dict() # {"model_name":weight}
        self.scores_ensemble=[(dict(),0.0,0.0),] # the auc score of the current ensemble for validation and holding 
    
    #==========================================================#
    def run(self):
        """Run the StepWise"""
        if not self.random:
            self.ensemble_models= self.the_k_best_models() # get the k best models
        else:
            self.ensemble_models= self.select_random_k_models() # get the k random models
        scv,sch=self.get_score_ensemble()
        self.scores_ensemble.append((self.ensemble_models.copy(),scv,sch))
        
        while True:
            md=self.select_one_model() # Add Model
            print "Add model -",md,"- ensemble and score:",self.scores_ensemble[-1]
            if md is None:
                print "Stop no model can increase score --------------"
                break
            
            last_score1= self.scores_ensemble[-1][1]
            last_score2= self.scores_ensemble[-2][1]
            #print last_score1,last_score2,"eps",math.fabs(last_score1-last_score2)
            if math.fabs(last_score1-last_score2)<=self.epslon:
                print "Stop epsilon  -------------------"
                break
                
            
            self.eliminate_one_model() # eliminate Model
            print "Elminate models -- ensemble and score:",self.scores_ensemble[-1]
            
            if len(self.ensemble_models.keys())>self.max_models:
                print "Stop max models ",self.max_models,"models ----------"
                break
        
    #==========================================================#
    def get_score_ensemble(self):
        """get validation and holding score"""
        probs_v,probs_h = None,None
        number_models=sum(self.ensemble_models.values())
        for model,weight in self.ensemble_models.items():
            if probs_v is None:
                probs_v=X_validation[model]*weight
            else:
                probs_v+=X_validation[model]*weight
            if probs_h is None:
                probs_h=X_holding[model]*weight
            else:
                probs_h+=X_holding[model]*weight
        #print "number",float(number_models)
        probs_v,probs_h = probs_v/float(number_models), probs_h/float(number_models)
        #print "is Nan",np.any(np.isnan(Y_validation))
        #print "is Inf",np.all(np.isfinite(Y_validation))
        fprv,tprv,llv=metrics.roc_curve(Y_validation, probs_v)
        score_v=metrics.auc(fprv, tprv)
        fprh,tprh,llh=metrics.roc_curve(Y_holding, probs_h)
        score_h=metrics.auc(fprh, tprh)
        
        return score_v,score_h
    
    #==========================================================#
    def select_one_model(self):
        """Method add a model wich maximize score: StepWise Selection"""
        choose_model=None
        score_max= self.scores_ensemble[-1][1]
        scr_v,scr_h=0,0
        
        for model in StepWiseAMH.all_models:
            self.add_model_in_ensemble(model)       # add model
            scr_vt,scr_ht=self.get_score_ensemble()
            if scr_vt>score_max:
                choose_model=model
                scr_v,scr_h=scr_vt,scr_ht
            
            self.delete_model_from_ensemble(model)  # delete the model
        
        if choose_model is not None:
            self.add_model_in_ensemble(choose_model)
            self.scores_ensemble.append((self.ensemble_models.copy(),scr_v,scr_h))# for the curve revolution score
        
        return choose_model
    
    #==========================================================#
    def eliminate_one_model(self):
        """Method elemine a model wich maximize score: StepWise Elemination"""
        models=self.ensemble_models.keys()
        choose_model=None
        score_max= self.scores_ensemble[-1][1]
        scr_v,scr_h=0,0
        
        if len(models)<2:
            return
        for model in models:
            ret=self.delete_model_from_ensemble(model,weighted=True)  # delete model
            scr_vt,scr_ht=self.get_score_ensemble()
            if scr_vt>score_max:
                choose_model=model
                scr_v,scr_h=scr_vt,scr_ht
            self.add_model_in_ensemble(model,weight=ret[1])      # add the model
            
        if choose_model is not None:
            ret=self.delete_model_from_ensemble(choose_model,weighted=True)
            self.scores_ensemble.append((self.ensemble_models.copy(),scr_v,scr_h))# for the curve revolution score
            
            self.eliminate_one_model() # continue elemination ...
        
    
    
    #==========================================================#
    def add_model_in_ensemble(self, model,weight=1):
        """Add a model in ensemble"""
        
        if model in self.ensemble_models:
            self.ensemble_models[model]+=1
        else:
            self.ensemble_models[model]=weight
                    
    #==========================================================#
    def delete_model_from_ensemble(self,model,weighted=False):
        """Delete one model"""
        if model in self.ensemble_models:
            if weighted==True:
                ret=(model,self.ensemble_models[model]) #return (model, weight)
                del self.ensemble_models[model]
                return ret
            if self.ensemble_models[model]>1:
                self.ensemble_models[model]-=1
            else:
                del self.ensemble_models[model]
    
    #==========================================================#
    def the_k_best_models(self):
        """Get the k best models by score auc"""
        ensemble=dict()
        with open("results/resultsProba/sortedClassifiers.txt","r") as fin:
            i=1
            for line in fin:
                model=line.split(":")[0]
                ensemble[model]=1
                if i>=self.k_best:
                    break
                i+=1
        return ensemble
    
    #==========================================================#
    def select_random_k_models(self):
        """Get the k random models"""
        ensemble=dict()
        n=len(StepWiseAMH.all_models)
        while len(ensemble) < self.k_best:
            ensemble[StepWiseAMH.all_models[randint(0,n-1)]]=1
        
        
  
              
