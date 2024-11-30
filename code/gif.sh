
IMAGE_DIR="dados/imagens_ppm"


OUTPUT_GIF="../../../docs/grafo.gif"


cd "$IMAGE_DIR" || exit


if ls frame_*.ppm 1> /dev/null 2>&1; then
    
    mkdir -p png_frames
    for img in frame_*.ppm; do
        ffmpeg -i "$img" "png_frames/${img%.ppm}.png"
    done

    
    ffmpeg -f image2 -framerate 10 -i png_frames/frame_%d.png -vf "scale=800:-1:flags=lanczos" -loop 0 "$OUTPUT_GIF"
    
    rm -r png_frames
    echo "GIF criado em $OUTPUT_GIF"
else
    echo "Nenhuma imagem PPM encontrada no diretório $IMAGE_DIR."
fi
