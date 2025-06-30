import scipy.stats as stats

r2_stl_abeta_train = [0.784175, 0.798659, 0.797461]
r2_stl_abeta_test = [0.789566, 0.743636, 0.746307]

mse_stl_abeta_train = [44672.107, 41560.402, 42114.983]
mse_stl_abeta_test = [45510.740, 57900.466, 55692.319]

rmse_stl_abeta_train = [211.358, 203.864, 205.219]
rmse_stl_abeta_test = [213.332, 240.625, 235.992]

r2_stl_ptau_train = [0.574860, 0.576860, 0.569942]
r2_stl_ptau_test = [0.519476, 0.506013, 0.540822]

mse_stl_ptau_train = [0.106090, 0.106979, 0.103773]
mse_stl_ptau_test = [0.100184, 0.096643, 0.109407]

rmse_stl_ptau_train = [0.325714, 0.327077, 0.322139]
rmse_stl_ptau_test = [0.316519, 0.310875, 0.330767]

r2_stl_tau_train = [0.492460, 0.467130, 0.487419]
r2_stl_tau_test = [0.401030, 0.509549, 0.419473]

mse_stl_tau_train = [0.101919, 0.105006, 0.105615]
mse_stl_tau_test = [0.112500, 0.100205, 0.097780]

rmse_stl_tau_train = [0.319248, 0.324047, 0.324985]
rmse_stl_tau_test = [0.335405, 0.316552, 0.312698]

r2_mtl_abeta_train = [0.728807, 0.699608, 0.707199]
r2_mtl_abeta_test = [0.659534, 0.765119, 0.741780]

mse_mtl_abeta_train = [56904.460, 61246.420, 60774.459]
mse_mtl_abeta_test = [72160.119, 54871.950, 56751.135]

rmse_mtl_abeta_train = [238.457, 247.480, 246.525]
rmse_mtl_abeta_test = [268.626, 234.248, 238.225]

r2_mtl_ptau_train = [0.578396, 0.574439, 0.577234]
r2_mtl_ptau_test = [0.546992, 0.559848, 0.551262]

mse_mtl_ptau_train = [0.101163, 0.100154, 0.101502]
mse_mtl_ptau_test = [0.110792, 0.114807, 0.109440]

rmse_mtl_ptau_train = [0.318061, 0.316472, 0.318594]
rmse_mtl_ptau_test = [0.332954, 0.338831, 0.330817]

r2_mtl_tau_train = [0.524212, 0.515629, 0.521129]
r2_mtl_tau_test = [0.485312, 0.514786, 0.497639]

mse_mtl_tau_train = [0.094507, 0.092842, 0.095563]
mse_mtl_tau_test = [0.100601, 0.107228, 0.096395]

rmse_mtl_tau_train = [0.307419, 0.304700, 0.309132]
rmse_mtl_tau_test = [0.317177, 0.327456, 0.310476]

_, p_value_abeta_r2 = stats.ttest_rel(r2_stl_abeta_test, r2_mtl_abeta_test)
_, p_value_ptau_r2 = stats.ttest_rel(r2_stl_ptau_test, r2_mtl_ptau_test)
_, p_value_tau_r2 = stats.ttest_rel(r2_stl_tau_test, r2_mtl_tau_test)

print(f"p-value based on R2 score for STL vs MTL ABETA prediction: {p_value_abeta_r2:2f}")
print(f"p-value based on R2 score for STL vs MTL PTAU prediction: {p_value_ptau_r2:2f}")
print(f"p-value based on R2 score for STL vs MTL TAU prediction: {p_value_tau_r2:2f}")

_, p_value_abeta_mse = stats.ttest_rel(mse_stl_abeta_test, mse_mtl_abeta_test)
_, p_value_ptau_mse = stats.ttest_rel(mse_stl_ptau_test, mse_mtl_ptau_test)
_, p_value_tau_mse = stats.ttest_rel(mse_stl_tau_test, mse_mtl_tau_test)

print(f"p-value based on MSE for STL vs MTL ABETA prediction: {p_value_abeta_mse:2f}")
print(f"p-value based on MSE for STL vs MTL PTAU prediction: {p_value_ptau_mse:2f}")
print(f"p-value based on MSE for STL vs MTL TAU prediction: {p_value_tau_mse:2f}")

_, p_value_abeta_rmse = stats.ttest_rel(rmse_stl_abeta_test, rmse_mtl_abeta_test)
_, p_value_ptau_rmse = stats.ttest_rel(rmse_stl_ptau_test, rmse_mtl_ptau_test)
_, p_value_tau_rmse = stats.ttest_rel(rmse_stl_tau_test, rmse_mtl_tau_test)
print(f"p-value based on RMSE for STL vs MTL ABETA prediction: {p_value_abeta_rmse:2f}")
print(f"p-value based on RMSE for STL vs MTL PTAU prediction: {p_value_ptau_rmse:2f}")
print(f"p-value based on RMSE for STL vs MTL TAU prediction: {p_value_tau_rmse:2f}")