# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# This program plots trended and de-trended crop yeild for Lee, Monroe, and
# Lancaster county; plots summer (June, July, August) averaged PDSI, 1 and 3
# month SPI, then calculates the correlation between the detrended crop yeild
# and the summer drought indices.
#
# Author: April Walker
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
library(plyr)
library(ggcorrplot)

# BEGIN var declarations
output_dir = "PDSI_output"
counties = c("Lancaster", "Monroe", "Lee")
drought_indicies = c("PDSI_m", "SPI_1_m", "SPI_3_m")

crop_files = c("Corn_Yield_Lancaster_county_Nebraska.txt",
               "Rice_Yield_Monroe_county_Arkansas.txt",
               "Soybeans_Yield_Lee_county_Arkansas.txt")

crop_yields = c("Corn yield (BU/Acre)", "Rice yield (LB/Acre)",
                "Soybeans yield (BU/Acre)")

crop_cols = matrix(nrow=0,ncol=4)
for (val in crop_yields) {
  crop_cols = rbind(crop_cols, c("Year", val, "Trend line", "Detrended vals"))
}


i = 1
while (i <= 3) {
  crop_files[i] = paste("Crop_yield/", crop_files[i], sep="")
  i = i + 1
}

crop_plots = c("Corn Yield in Lancaster County",
               "Rice Yield in Monroe County",
               "Soybean Yield in Lee County")
# END var declarations

# plot crop yeilds
i = 1
lancaster = monroe = lee = data.frame("Year" = c(1981:2016))

for (val in crop_files) {
  data = read.table(file=val, header=FALSE)
  names(data) = crop_cols[i,]
  # plot crop yeild trends for each region
  jpeg(paste(counties[i], "_crop_trend.jpeg"))
  plot(data[,1], data[,2], main = crop_plots[i], xlab = colnames(data)[1],
        ylab = colnames(data)[2], col = "#6C48B5")
  print(counties[i])
  fit = lm(data[,2] ~ data[,1])
  print(summary(fit))
  lines(data[,1], data[,3], col = "#367C5E")
  dev.off()
  # add location data to correct dataframe
  if (i == 1) {
    lancaster = cbind(lancaster, data[,2])
  } else if (i == 2) {
    monroe = cbind(monroe, data[,2])
  } else {
    lee = cbind(lee, data[,2])
    names(lee[1,]) = crop_cols[i,2]
  }
  i = i + 1
}


# add all files we need to calculates
drought_files = character()
drought_plots = character()
drought_titles = character()
for (val in counties) {
  for (indices in drought_indicies) {
    drought_files = append(drought_files, paste(output_dir, "/sc", indices,
        "_", val, ".clm", sep=""))
    drought_plots = append(drought_plots, paste(val, indices, ".jpeg", sep=""))
    drought_titles = append(drought_titles, paste(val, indices, sep=" "))

  }
}

i = 1
for (val in drought_files) {
  data = read.table(file=val, header=TRUE)
  summer_data = subset(data, Per %in% c(6, 7, 8))
  summer_data = aggregate(summer_data, by=list(summer_data$Year), mean)
  # below dataframe contains avg summer drought indices for each year
  summer_data = summer_data[,c(2,4)]
  # plot summer avg drought indices for each region
  jpeg(paste(drought_plots[i]))
  plot(summer_data[,1], summer_data[,2], main = drought_titles[i],
      xlab = colnames(summer_data)[1], ylab = colnames(summer_data)[2],
      col = "#6C48B5", type="b")
  trend = lm(summer_data[,2] ~ summer_data[,1])
  abline(trend, col = "#367C5E")
  dev.off()
  if (i <= 3) {
    lancaster = cbind(lancaster, summer_data[,2])
    names(lancaster)[2] = crop_cols[1,2]
  } else if (i <= 6) {
    monroe = cbind(monroe, summer_data[,2])
    names(monroe)[2] = crop_cols[2,2]
  } else {
    lee = cbind(lee, summer_data[,2])
    names(lee)[2] = crop_cols[3,2]
  }

  i = i + 1
}

names(lancaster)[3:5] = names(monroe)[3:5] = names(lee)[3:5] =
    drought_indicies

corr_m = round(cor(lancaster), 2)
p.mat = cor_pmat(lancaster)
round(corr_m, 2)
jpeg("lancaster_corr.jpeg")
print(ggcorrplot(corr_m, title = "Lancaster Crop/Drought Correlation",
  p.mat = p.mat, lab = TRUE,
    outline.col = "white",
    ggtheme = ggplot2::theme_gray,
    colors = c("#367C5E", "white", "#6C48B5"))
    + theme(plot.title = element_text(size = 14, face="bold", hjust=0.5, vjust=1)))
dev.off()

jpeg("lancaster_comp.jpeg")
par(mar=c(5, 12, 4, 4) + 0.1)
plot(lancaster[,1], lancaster[,2], axes = F, main="Lancaster PDSI and Corn Yield vs Year",
    type="b", col = "#367C5E", xlab="", ylab="")
axis(2, ylim=c(min(lancaster[,2]),max(lancaster[,2])), col="black", lwd=1)
mtext(2, text="Corn Yield", line=2)
par(new=T)
plot(lancaster[,1], lancaster[,3], col="#6C48B5", axes = F,
    ylim=c(min(lancaster[,3]),max(lancaster[,3])),
    type="b", xlab="", ylab="", lty = 2)
axis(2, ylim=c(min(lancaster[,3]),max(lancaster[,3])), col="black", line=3.5)
mtext(2, text="PDSI", line=5.5)
axis(1,pretty(range(lancaster[,1]),10))
legend(x="topleft", legend=c("Corn Yield", "PDSI"), col=c("#367C5E","#6C48B5"),
    lty=c(1,2))
dev.off()

fit = lm(lancaster[,2] ~ lancaster[,3])
print(summary(fit))

corr_m = round(cor(monroe), 2)
p.mat = cor_pmat(monroe)
round(corr_m, 2)
jpeg("monroe_corr.jpeg")
print(ggcorrplot(corr_m, title = "Monroe Crop/Drought Correlation",
  p.mat = p.mat, lab = TRUE,
    outline.col = "white",
    ggtheme = ggplot2::theme_gray,
    colors = c("#367C5E", "white", "#6C48B5"))
    + theme(plot.title = element_text(size = 14, face="bold", hjust=0.5, vjust=1)))
dev.off()

jpeg("monroe_comp.jpeg")
par(mar=c(5, 12, 4, 4) + 0.1)
plot(monroe[,1], monroe[,2], axes = F, main="Monroe SPI-1 and Rice Yield vs Year",
    type="b", col = "#367C5E", xlab="", ylab="")
axis(2, ylim=c(min(monroe[,2]),max(monroe[,2])), col="black", lwd=1)
mtext(2, text="Rice Yield", line=2)
par(new=T)
plot(monroe[,1], monroe[,4], col="#6C48B5", axes = F,
    ylim=c(min(monroe[,4]),max(monroe[,4])),
    type="b", xlab="", ylab="", lty = 2)
axis(2, ylim=c(min(monroe[,4]),max(monroe[,4])), col="black", line=3.5)
mtext(2, text="SPI-1", line=5.5)
axis(1,pretty(range(monroe[,1]),10))
legend(x="bottomright", legend=c("Rice Yield", "SPI-1"), col=c("#367C5E","#6C48B5"),
    lty=c(1,2))
dev.off()

fit = lm(monroe[,2] ~ monroe[,4])
print(summary(fit))

corr_m = round(cor(lee), 2)
p.mat = cor_pmat(lee)
jpeg("lee_corr.jpeg")
print(ggcorrplot(corr_m, title = "Lee Crop/Drought Correlation",
  p.mat = p.mat, lab = TRUE,
    outline.col = "white",
    ggtheme = ggplot2::theme_gray,
    colors = c("#367C5E", "white", "#6C48B5"))
    + theme(plot.title = element_text(size = 14, face="bold", hjust=0.5, vjust=1)))
dev.off()

jpeg("lee_comp.jpeg")
par(mar=c(5, 12, 4, 4) + 0.1)
plot(lee[,1], lee[,2], axes = F, main="Lee PDSI and Soybean Yield vs Year",
    type="b", col = "#367C5E", xlab="", ylab="")
axis(2, ylim=c(min(lee[,2]),max(lee[,2])), col="black", lwd=1)
mtext(2, text="Soybean Yield", line=2)
par(new=T)
plot(lee[,1], lee[,4], col="#6C48B5", axes = F,
    ylim=c(min(lee[,4]),max(lee[,4])),
    type="b", xlab="", ylab="", lty = 2)
axis(2, ylim=c(min(lee[,4]),max(lee[,4])), col="black", line=3.5)
mtext(2, text="SPI-1", line=5.5)
axis(1,pretty(range(lee[,1]),10))
legend(x="bottomleft", legend=c("Soybean Yield", "SPI-1"), col=c("#367C5E","#6C48B5"),
    lty=c(1,2))
dev.off()

fit = lm(lee[,2] ~ lee[,4])
print(summary(fit))
