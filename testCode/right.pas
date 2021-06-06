program zcrProgram;
var i, j, k: integer;
    number, sum: real;
// var color: real;
begin
	// i := -7;
	// k := i*9 + 1;
	// // p := 404;
	/** abc*d**/
	j := (9 + 3) - 8;
	i := 4;
	for i := 1 to 10 do
	begin
		j := (j + 2) * ((i + 6) - 10) + 4;
		// j := j - 5;
		if (j > 13)
		then
			continue;
		j := j + 3;
		if (j = 7)
		then
			break
		else
			j := j * 3;
	end;
end.
