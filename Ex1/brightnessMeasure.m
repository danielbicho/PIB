function [ m ] = brightnessMeasure( I )

if nargin == 0
    I = imread( '..\Exer_2\Medical_Images\1_PET1.tif' );
%   I = imread( '..\Exer_2\Medical_Images\3.png' );
end

[M, N]=size(I);
m = sum( sum( I ) )/M*N;

end
