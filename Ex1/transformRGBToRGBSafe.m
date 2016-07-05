function transformRGBToRGBSafe( filename )

I = imread( filename );

safe_colors = getSafeColors();
[M N K] = size( I );
Ip = zeros( M, N, K,'uint8' );
pixel_write = zeros(1,1,K);

for i=1:M
    for j=1:N
        pixel_read = I(i,j,:);
        pixel_read = [pixel_read(1,1,1),pixel_read(1,1,2),pixel_read(1,1,3)];
        pixel_write_aux = getNearestPixel( double(pixel_read), safe_colors );
        pixel_write(1,1,:)=pixel_write_aux(1,:);
        Ip(i,j,:)=pixel_write;
    end
end
f = strsplit(filename,'.');
newName = strcat(f{1}, '_safeColors.', f{2} );
imwrite(Ip, newName);

countUniqueColors(filename );
countUniqueColors(newName );

figure(1);
subplot(121); imshow(I); colorbar; title(' Imagem original' );
subplot(122); imshow(Ip); colorbar; title(' Imagem safe color' );
impixelinfo;


    
function p_write = getNearestPixel( p_read, safe_colors )

p_write = [];
for i=1:3
    dist=abs(safe_colors(:,i) - p_read(:,i));
    [m idx] = min(dist);
    p_write = [ p_write, safe_colors(idx,i)];
end
p_write = uint8(p_write);


