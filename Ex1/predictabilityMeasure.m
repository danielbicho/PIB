function [ H ] = predictability( I )

if nargin == 0
    I = imread( '..\Exer_2\Medical_Images\1_PET1.tif' );
%   I = imread( '..\Exer_2\Medical_Images\3.png' );
end

[M, N] = size(I);

[ counts, x ] = imhist(I);

probability = counts/(M*N);

probability( probability == 0 ) = 1;

H = -sum(probability .* log2( probability ) );

% J = entropy(I)
end
