function countUniqueColors( filename ) 

I = imread( filename );

safe_colors = getSafeColors();

[M N K] = size( I );
colors = [];
safe_color = true;
for l=1:M
   for c=1:N
        colors = addIfNewColor(  I(l,c,1), I(l,c,2), I(l,c,3), colors);
        if safe_color
            safe_color = checkIfSafeColor( [I(l,c,1), I(l,c,2), I(l,c,3)], safe_colors );
        end;
   end
end
fprintf( 'Ficheiro: %s\n', filename );
fprintf( 'Resolução: %i x %i, %i\n', M, N, M*N );
fprintf( 'Nº de cores: %d\n', size(colors,1) );
fprintf( 'Image RGB safe: %i\n', safe_color );


function [ colors] = addIfNewColor( shadeR, shadeG, shadeB, colors)

numColors = size(colors,1);
newColor = true;
for i=1:numColors
    if colors(i,:)==[shadeR, shadeG, shadeB]
        newColor = false;
        break;
    end
end

if newColor
    colors = [colors;[shadeR, shadeG, shadeB]];
end
    
function [ safe_color ] = checkIfSafeColor( rgbColor, safe_colors)

safe_color = false;
numColors = size( safe_colors, 1);
for i=1:numColors
    if rgbColor == safe_colors(i,:)
        safe_color = true;
        return
    end
end
return

