module try (
    input  in1,
    input  in2,
    output reg out3
);

always@(*) begin
    if(in1) begin
        out3 = in1;
    end
    else if(in2) begin
        out3 = in2;
    end
    else 
        out3 = 0; 
end
endmodule
