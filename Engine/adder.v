module adder(
    input [3:0] in1,
    input [3:0] in2,
    input [1:0] in3,
    input       clk,rst,
    output reg [3:0] out,out2,out3,out4,out1,out5,out9,out6
);
    wire  [1:0]  internOut;

    reg   [3:0]  current_state, current_state_2, current_state_3, current_state_4;
    
    reg   [1:0]  current_state_5, state;

    assign internOut = (in1*in2*in1);

    localparam [3:0]      idle=4'b0000,             //s0
                      blance_check=4'b0001,     //s1
					  withdraw=4'b0010,         //s2
					  deposit=4'b0011,          //s3
					  transfer=4'b0100, 		//s4
					  exit=4'b0101,             //s5
					  new_pass=4'b0110,         //s6
					  lang_used=4'b0111,        //s7
					  scan_card=4'b1000,         //s8
					  enter_pass=4'b1001,       //s9
					  option_select=4'b1010,    //s10 
					  anything_else=4'b1011;    //s11
    
    localparam [1:0]  S0 = 2'b00,
                      S1 = 2'b01,
                      S2 = 2'b10,
                      S3 = 2'b11;

    always@(posedge clk or negedge rst) 
    begin   
        if(rst)
            current_state_2 <= 4'b0;
        else begin
            current_state <= in1;
            current_state_2 <= 4'b0;
        end
    end

    always@(posedge clk) begin
        case(current_state)
        idle : current_state_3 <= 4'b0;
        transfer : begin
            current_state_3 <= in1;
            current_state_4 <= in2;
        end
        endcase
    end

    always @(*) begin
        case(in3)
        2'b00 : out6 = 0;
        2'b01 : out6 = 1;
        2'b10 : out6 = 2;
        endcase
    end

    always@(posedge clk or negedge rst) begin
        if(!rst) begin
            current_state_5 <= 2'b0;
        end
        else begin
            current_state_5 <= state;
        end
    end

    always@(*) begin
        case(current_state_5)
        S0 : state = S1;
        S1 : state = S2;
        S2 : state = S1;
        S3 : state = S0;
        endcase
    end


    always@(*) begin
        if(current_state_2 == 0) begin
            out1 = in1;
        end
        else begin
            out1 = in2;
        end
    end

    always@(*)
    begin
        if(in1 & in2) begin
            out3 = in1;
            if(in2 > in1) begin
                out1 = 1;
            end
        end
        else begin
            out1 = 3;
            out2 = in2;
        end
    end

    always@(*) begin
        out1 = in2 ==in1;
        out2 = in1+in1;
        out3 = in2*in1;
        if(in1==in2)
        begin
            if(^in2)
                out = |in1;
            else
                out = |in2;
            out = &(in1*in2);
            out3 = |(in1+in2);
            if(in1 >= in2) begin
                out4 = in1/in2;
            end
            else if(in1&in2)
                begin
                    out=|in2;
                    out2 =& in2;
                end
            else
                out3 = | ( in1+in2 );
        end
        else if(in1>in2)
            out = in1>>2;
        else begin
            out2= ^(in1*in2);
            out4 = in1<<2;
        end
        out4 = in1&in2&out3;
        case(in1&in2)
        blance_check : begin
                    out4 = in1<<2;
                    out2 = in2*in1;
        end
        default: out4 = 0;
        endcase
    end
    always@(*) begin
        out1 = in2 ==in1;
        out2 = in1+in1;
        out5 = in2*in1;
        if(in1==in2)
        begin
            if(^in2)
                out = |in1;
            else
                out = |in2;
            out = &(in1*in2);
            out5 = |(in1+in2);
            if(in1 >= in2) begin
                out4 = in1/in2;
            end
            else if(in1&in2)
                begin
                    out=|in2;
                    out2 =& in2;
                end
            else
                out5 = | ( in1+in2 );
        end
        else if(in1>in2)
            out = in1>>2;
        else begin
            out2= ^(in1*in2);
            out4 = in1<<2;
        end
        out4 = in1&in2&out3;
        case(in1&in2)
        blance_check : begin
                    out4 = in1<<2;
                    out2 = in2*in1;
        end
        default: out4 = 0;
        endcase
    end

        always@(*) begin
        out1 = in2 ==in1;
        out2 = in1+in1;
        out5 = in2*in1;
        if(in1==in2)
        begin
            if(^in2)
                out = |in1;
            else
                out = |in2;
            out = &(in1*in2);
            out5 = |(in1+in2);
            if(in1 >= in2) begin
                out4 = in1/in2;
            end
            else if(in1&in2)
                begin
                    out=|in2;
                    out2 =& in2;
                end
            else
                out5 = | ( in1+in2 );
        end
        else if(in1>in2)
            out = in1>>2;
        else begin
            out2= ^(in1*in2);
            out4 = in1<<2;
        end
        out4 = in1&in2&out3;
        case(in1&in2)
        blance_check : begin
                    out4 = in1<<2;
                    out2 = in2*in1;
                    out9 = in2*in1;
        end
        default: out4 = 0;
        endcase
    end
endmodule

    