function face_2()

addpath('.\colorImages','-end');
addpath('.\..\LP2_utils','-end');

IO = imread( 'face.jpg' );
IN = imread( 'face_2.jpg' );

IO_R = IO(:,:,1);
IO_G = IO(:,:,2);
IO_B = IO(:,:,3);

figure(1); set(gcf,'Name', 'Imagem original');
subplot(221); imshow(IO);
subplot(222); imshow(IO_R); title('R');
subplot(223); imshow(IO_G); title('G');
subplot(224); imshow(IO_B); title('B');

IN_R = IN(:,:,1);
IN_G = IN(:,:,2);
IN_B = IN(:,:,3);


figure(2); set(gcf,'Name', 'Imagem original-histogramas');
subplot(221); imhist(IO_R); title('R');
subplot(222); imhist(IO_G); title('G');
subplot(223); imhist(IO_B); title('B');




difBright_IO_IN = difBrightnessColor( IO, IN );
fprintf( ' Dif. de brilho face - face_2:%d\n', difBright_IO_IN );
difContr_IO_IN = difContrastColor( IO, IN, 20 );
fprintf( ' Dif de contraste face - face_2:%d\n', difContr_IO_IN );
difEntropy_IO_IN = difPredictabilityColor( IO, IN );
fprintf( ' Dif. de entropia face - face_2:%d\n', difEntropy_IO_IN );


figure(3); set(gcf,'Name', 'Imagem problemática');
subplot(221); imshow(IN);
subplot(222); imshow(IN_R); title('R');
subplot(223); imshow(IN_G); title('G');
subplot(224); imshow(IN_B); title('B');

figure(4); set(gcf,'Name', 'Imagem problemática-histogramas');
subplot(221); imhist(IN_R); title('R');
subplot(222); imhist(IN_G); title('G');
subplot(223); imhist(IN_B); title('B');


LUT_R = contrast_streching_band( double(min(min(IN_R))), double(max(max(IN_R))),0,double(max(max(IN_R))));
IN2_R_p = intlut( IN_R, LUT_R);

LUT_G = contrast_streching_band( double(min(min(IN_G))), double(max(max(IN_G))),0,double(max(max(IN_G))));
IN2_G_p = intlut( IN_G, LUT_G);

LUT_B = contrast_streching_band( double(min(min(IN_B))), double(max(max(IN_B))),0,double(max(max(IN_B))));
IN2_B_p = intlut( IN_B, LUT_B);

IF = IN;
IF(:,:,1) = IN2_R_p;
IF(:,:,2) = IN2_G_p;
IF(:,:,3) = IN2_B_p;

figure(5); set(gcf,'Name', 'Imagem problemática-histogramas processados');
subplot(221); imhist(IN2_R_p); title('R');
subplot(222); imhist(IN2_G_p); title('G');
subplot(223); imhist(IN2_B_p); title('B');

figure(6); set(gcf,'Name', 'I processado');
subplot(221); imshow(IN2_R_p); colorbar; title('R' );
subplot(222); imshow(IN2_G_p); colorbar; title('G' );
subplot(223); imshow(IN2_B_p); colorbar; title('B' );
subplot(224); imshow(IF); colorbar; title('Imagem final' );

difBright_IO_IF = difBrightnessColor( IO, IF );
fprintf( '\nDif. de brilho face - face_F:%d\n', difBright_IO_IF );
difContr_IO_IF = difContrastColor( IO, IF, 20 );
fprintf( ' Dif. de contraste face - face_F:%d\n', difContr_IO_IF );
difEntropy_IO_IF = difPredictabilityColor( IO, IF );
fprintf( ' Dif. de entropia face - face_F:%d\n', difEntropy_IO_IF );

figure(7);
subplot(121); imshow(IO); title('I original' );
subplot(122); imshow(IF); title('I processed' );




