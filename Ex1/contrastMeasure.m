function [ cI ] = contrastMeasure( I, B )

if nargin == 0
    I = imread( '..\Exer_2\Medical_Images\1_PET1.tif' );
%   I = imread( '..\Exer_2\Medical_Images\3.png' );
    B = 30;
end
[ blocks ]= divide_image( I, B );
B = size( blocks, 3);
cI = 0;
for b=1:B
    mx = max(max( blocks(:,:, b )));
    mi = min(min( blocks(:,:, b )));
    if mx ~= 0
        cI = cI + 20*log10(mx/(1+mi))/B; 
    end
end
end

