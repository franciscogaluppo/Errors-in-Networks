function mat = ler(nome, run)
	path = strcat("../ZF/NOVOS/ZF_", nome, "_", num2str(run), ".txt");
	mat = dlmread(path);
end
