import scipy.stats as stats

# ----------------------------------------------------------------------------------
# MTL

# Target 1 (abeta)
r2_mtl_abeta_train = [0.9097, 0.9214, 0.9029][:3]
r2_mtl_abeta_test = [0.5802, 0.6284, 0.6341][:3]

mse_mtl_abeta_train = [0.0917, 0.0770, 0.0976][:3]
mse_mtl_abeta_test = [0.3920, 0.4018, 0.3580][:3]

rmse_mtl_abeta_train = [0.3029, 0.2774, 0.3124][:3]
rmse_mtl_abeta_test = [0.6261, 0.6339, 0.5983][:3]

# Target 2 (ptau)
r2_mtl_ptau_train = [0.7643, 0.8463, 0.7623][:3]
r2_mtl_ptau_test = [0.4452, 0.3835, 0.4828][:3]

mse_mtl_ptau_train = [0.2278, 0.1500, 0.2353][:3]
mse_mtl_ptau_test = [0.6160, 0.6743, 0.5362][:3]

rmse_mtl_ptau_train = [0.4773, 0.3873, 0.4850][:3]
rmse_mtl_ptau_test = [0.7849, 0.8212, 0.7323][:3]

# Target 3 (tau)
r2_mtl_tau_train = [0.6848, 0.7836, 0.6865][:3]
r2_mtl_tau_test = [0.3631, 0.3113, 0.4226][:3]

mse_mtl_tau_train = [0.3038, 0.2092, 0.3136][:3]
mse_mtl_tau_test = [0.7159, 0.7795, 0.5748][:3]

rmse_mtl_tau_train = [0.5512, 0.4574, 0.5600][:3]
rmse_mtl_tau_test = [0.8461, 0.8829, 0.7581][:3]

# ----------------------------------------------------------------------------------
# STL

# Target 1 (abeta)
r2_stl_abeta_train = [0.9987, 0.9986, 0.9984, 0.9982][:3]
r2_stl_abeta_test = [0.6511, 0.6208, 0.6257, 0.6413][:3]

mse_stl_abeta_train = [0.0013, 0.0014, 0.0016, 0.0018][:3]
mse_stl_abeta_test = [0.3308, 0.4101, 0.3663, 0.3636][:3]

rmse_stl_abeta_train = [0.0366, 0.0370, 0.0397, 0.0419][:3]
rmse_stl_abeta_test = [0.5752, 0.6404, 0.6052, 0.6030][:3]

# Target 2 (ptau)
r2_stl_tau_train = [0.9797, 0.9898, 0.9824, 0.9752, 0.9827, 0.9846][:3]
r2_stl_tau_test = [0.4255, 0.3179, 0.3296, 0.3921, 0.3544, 0.2969][:3]

mse_stl_tau_train = [0.0203, 0.0099, 0.0172, 0.0245, 0.0167, 0.0149][:3]
mse_stl_tau_test = [0.5720, 0.7442, 0.7228, 0.6414, 0.7258, 0.7958][:3]

rmse_stl_tau_train = [0.1424, 0.0997, 0.1312, 0.1565, 0.1293, 0.1219][:3]
rmse_stl_tau_test = [0.7563, 0.8627, 0.8502, 0.8009, 0.8519, 0.8921][:3]

# Target 3 (tau)
r2_stl_ptau_train = [0.9902, 0.9908, 0.9867, 0.9839][:3]
r2_stl_ptau_test = [0.3662, 0.3662, 0.4145, 0.4224][:3]

mse_stl_ptau_train = [0.0023, 0.0022, 0.0031, 0.0037][:3]
mse_stl_ptau_test = [0.1673, 0.1673, 0.1569, 0.1548][:3]

rmse_stl_ptau_train = [0.0480, 0.0471, 0.0558, 0.0612][:3]
rmse_stl_ptau_test = [0.4090, 0.4090, 0.3961, 0.3934][:3]

# --------------------------------------------------------------------------------------
# Statistical significance tests

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

r2_mean_abeta_stl, r2_error_bar_abeta_stl = stats.tmean(r2_stl_abeta_test), stats.sem(r2_stl_abeta_test)
r2_mean_abeta_mtl, r2_error_bar_abeta_mtl = stats.tmean(r2_mtl_abeta_test), stats.sem(r2_mtl_abeta_test)
r2_mean_ptau_stl, r2_error_bar_ptau_stl = stats.tmean(r2_stl_ptau_test), stats.sem(r2_stl_ptau_test)
r2_mean_ptau_mtl, r2_error_bar_ptau_mtl = stats.tmean(r2_mtl_ptau_test), stats.sem(r2_mtl_ptau_test)
r2_mean_tau_stl, r2_error_bar_tau_stl = stats.tmean(r2_stl_tau_test), stats.sem(r2_stl_tau_test)
r2_mean_tau_mtl, r2_error_bar_tau_mtl = stats.tmean(r2_mtl_tau_test), stats.sem(r2_mtl_tau_test)

mse_mean_abeta_stl, mse_error_bar_abeta_stl = stats.tmean(mse_stl_abeta_test), stats.sem(mse_stl_abeta_test)
mse_mean_abeta_mtl, mse_error_bar_abeta_mtl = stats.tmean(mse_mtl_abeta_test), stats.sem(mse_mtl_abeta_test)
mse_mean_ptau_stl, mse_error_bar_ptau_stl = stats.tmean(mse_stl_ptau_test), stats.sem(mse_stl_ptau_test)
mse_mean_ptau_mtl, mse_error_bar_ptau_mtl = stats.tmean(mse_mtl_ptau_test), stats.sem(mse_mtl_ptau_test)
mse_mean_tau_stl, mse_error_bar_tau_stl = stats.tmean(mse_stl_tau_test), stats.sem(mse_stl_tau_test)
mse_mean_tau_mtl, mse_error_bar_tau_mtl = stats.tmean(mse_mtl_tau_test), stats.sem(mse_mtl_tau_test)

rmse_mean_abeta_stl, rmse_error_bar_abeta_stl = stats.tmean(rmse_stl_abeta_test), stats.sem(rmse_stl_abeta_test)
rmse_mean_abeta_mtl, rmse_error_bar_abeta_mtl = stats.tmean(rmse_mtl_abeta_test), stats.sem(rmse_mtl_abeta_test)
rmse_mean_ptau_stl, rmse_error_bar_ptau_stl = stats.tmean(rmse_stl_ptau_test), stats.sem(rmse_stl_ptau_test)
rmse_mean_ptau_mtl, rmse_error_bar_ptau_mtl = stats.tmean(rmse_mtl_ptau_test), stats.sem(rmse_mtl_ptau_test)
rmse_mean_tau_stl, rmse_error_bar_tau_stl = stats.tmean(rmse_stl_tau_test), stats.sem(rmse_stl_tau_test)
rmse_mean_tau_mtl, rmse_error_bar_tau_mtl = stats.tmean(rmse_mtl_tau_test), stats.sem(rmse_mtl_tau_test)

print('' + '-' * 50)
print(f"R2 ABETA STL: {r2_mean_abeta_stl:.4f} ± {r2_error_bar_abeta_stl:.4f}")
print(f"R2 ABETA MTL: {r2_mean_abeta_mtl:.4f} ± {r2_error_bar_abeta_mtl:.4f}")
print(f"R2 PTAU STL: {r2_mean_ptau_stl:.4f} ± {r2_error_bar_ptau_stl:.4f}")
print(f"R2 PTAU MTL: {r2_mean_ptau_mtl:.4f} ± {r2_error_bar_ptau_mtl:.4f}")
print(f"R2 TAU STL: {r2_mean_tau_stl:.4f} ± {r2_error_bar_tau_stl:.4f}")
print(f"R2 TAU MTL: {r2_mean_tau_mtl:.4f} ± {r2_error_bar_tau_mtl:.4f}")
print('' + '-' * 50)
print(f"MSE ABETA STL: {mse_mean_abeta_stl:.4f} ± {mse_error_bar_abeta_stl:.4f}")
print(f"MSE ABETA MTL: {mse_mean_abeta_mtl:.4f} ± {mse_error_bar_abeta_mtl:.4f}")
print(f"MSE PTAU STL: {mse_mean_ptau_stl:.4f} ± {mse_error_bar_ptau_stl:.4f}")
print(f"MSE PTAU MTL: {mse_mean_ptau_mtl:.4f} ± {mse_error_bar_ptau_mtl:.4f}")
print(f"MSE TAU STL: {mse_mean_tau_stl:.4f} ± {mse_error_bar_tau_stl:.4f}")
print(f"MSE TAU MTL: {mse_mean_tau_mtl:.4f} ± {mse_error_bar_tau_mtl:.4f}")
print('' + '-' * 50)
print(f"RMSE ABETA STL: {rmse_mean_abeta_stl:.4f} ± {rmse_error_bar_abeta_stl:.4f}")
print(f"RMSE ABETA MTL: {rmse_mean_abeta_mtl:.4f} ± {rmse_error_bar_abeta_mtl:.4f}")
print(f"RMSE PTAU STL: {rmse_mean_ptau_stl:.4f} ± {rmse_error_bar_ptau_stl:.4f}")
print(f"RMSE PTAU MTL: {rmse_mean_ptau_mtl:.4f} ± {rmse_error_bar_ptau_mtl:.4f}")
print(f"RMSE TAU STL: {rmse_mean_tau_stl:.4f} ± {rmse_error_bar_tau_stl:.4f}")
print(f"RMSE TAU MTL: {rmse_mean_tau_mtl:.4f} ± {rmse_error_bar_tau_mtl:.4f}")