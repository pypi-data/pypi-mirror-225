import os
import pandas as pd
import numpy as np
from neuroCombat import neuroCombat
data = np.genfromtxt(os.path.join('inputData' , 'testdata.csv'), delimiter=",", skip_header=1)
categorical_cols = ['gender']
batch_col = 'batch'
print(data)
raise IOError




covars = {'batch':[1,1,1,1,1,2,2,2,2,2], 'gender':[1,2,1,2,1,2,1,2,1,2]}
covars = pd.DataFrame(covars)
# Adjusted + Parametric
data_combat = neuroCombat(dat=data,covars=covars,batch_col=batch_col,categorical_cols=categorical_cols)
np.savetxt('outputData/testdata_combat_parametric_adjusted_python.csv', data_combat, delimiter=',')
# Adjusted + Parametric +NoEB
data_combat = neuroCombat(dat=data,covars=covars,batch_col=batch_col,categorical_cols=categorical_cols,eb=False)
np.savetxt('outputData/testdata_combat_parametric_adjusted_noeb_python.csv', data_combat, delimiter=',')
# Adjusted + NonParametric
data_combat = neuroCombat(dat=data,covars=covars,batch_col=batch_col,categorical_cols=categorical_cols,parametric=False)
np.savetxt('outputData/testdata_combat_nonparametric_adjusted_python.csv', data_combat, delimiter=',')
# Adjusted + NonParametric + NoEB
data_combat = neuroCombat(dat=data,covars=covars,batch_col=batch_col,categorical_cols=categorical_cols,eb=False,parametric=False)
np.savetxt('outputData/testdata_combat_nonparametric_adjusted_noeb_python.csv', data_combat, delimiter=',')



covars = {'batch':[1,1,1,1,1,2,2,2,2,2]}
covars = pd.DataFrame(covars)
# Unadjusted + Parametric
data_combat = neuroCombat(dat=data,covars=covars,batch_col=batch_col)
np.savetxt('outputData/testdata_combat_parametric_unadjusted_python.csv', data_combat, delimiter=',')
# Unadjusted + Parametric + NoEB
data_combat = neuroCombat(dat=data,covars=covars,batch_col=batch_col,eb=False)
np.savetxt('outputData/testdata_combat_parametric_unadjusted_noeb_python.csv', data_combat, delimiter=',')
# Unadjusted + NonParametric
data_combat = neuroCombat(dat=data,covars=covars,batch_col=batch_col,parametric=False)
np.savetxt('outputData/testdata_combat_nonparametric_unadjusted_python.csv', data_combat, delimiter=',')
# Unadjusted + NonParametric + NoEB
data_combat = neuroCombat(dat=data,covars=covars,batch_col=batch_col,eb=False,parametric=False)
np.savetxt('outputData/testdata_combat_nonparametric_unadjusted_noeb_python.csv', data_combat, delimiter=',')





######## Mean only True
# Adjusted + Parametric
covars = {'batch':[1,1,1,1,1,2,2,2,2,2], 'gender':[1,2,1,2,1,2,1,2,1,2]}
covars = pd.DataFrame(covars)
data_combat = neuroCombat(dat=data,covars=covars,batch_col=batch_col,categorical_cols=categorical_cols,mean_only=True)
np.savetxt('outputData/testdata_combat_parametric_adjusted_meanonly_python.csv', data_combat, delimiter=',')
data_combat = neuroCombat(dat=data,covars=covars,batch_col=batch_col,categorical_cols=categorical_cols,parametric=False,mean_only=True)
np.savetxt('outputData/testdata_combat_nonparametric_adjusted_meanonly_python.csv', data_combat, delimiter=',')
data_combat = neuroCombat(dat=data,covars=covars,batch_col=batch_col,categorical_cols=categorical_cols,parametric=True,eb=False,mean_only=True)
np.savetxt('outputData/testdata_combat_parametric_adjusted_noeb_meanonly_python.csv', data_combat, delimiter=',')
data_combat = neuroCombat(dat=data,covars=covars,batch_col=batch_col,categorical_cols=categorical_cols,parametric=False,eb=False,mean_only=True)
np.savetxt('outputData/testdata_combat_nonparametric_adjusted_noeb_meanonly_python.csv', data_combat, delimiter=',')


######## Mean only True
# UnAdjusted + Parametric
covars = {'batch':[1,1,1,1,1,2,2,2,2,2], 'gender':[1,2,1,2,1,2,1,2,1,2]}
covars = pd.DataFrame(covars)
data_combat = neuroCombat(dat=data, covars=covars,batch_col=batch_col,mean_only=True)
np.savetxt('outputData/testdata_combat_parametric_unadjusted_meanonly_python.csv', data_combat, delimiter=',')
data_combat = neuroCombat(dat=data,covars=covars,batch_col=batch_col,parametric=False,mean_only=True)
np.savetxt('outputData/testdata_combat_nonparametric_unadjusted_meanonly_python.csv', data_combat, delimiter=',')
data_combat = neuroCombat(dat=data,covars=covars,batch_col=batch_col,parametric=True,eb=False,mean_only=True)
np.savetxt('outputData/testdata_combat_parametric_unadjusted_noeb_meanonly_python.csv', data_combat, delimiter=',')
data_combat = neuroCombat(dat=data,covars=covars,batch_col=batch_col,parametric=False,eb=False,mean_only=True)
np.savetxt('outputData/testdata_combat_nonparametric_unadjusted_noeb_meanonly_python.csv', data_combat, delimiter=',')
