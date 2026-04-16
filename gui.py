import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from inputs import MixInputs
from mix_design import MixDesign

def run_calculation():
    try:
        if int(slump_var.get()) <= 0:
            raise ValueError("Slump must be positive")

        inputs = MixInputs(
            grade=grade_var.get(),
            exposure=exposure_var.get(),
            aggregate_size=int(agg_size_var.get()),
            slump=int(slump_var.get()),
            sand_zone=sand_zone_var.get(),
            aggregate_type=agg_type_var.get()
        )

        mix = MixDesign(inputs)
        result = mix.generate_mix(print_steps=False)

        output_text.delete(1.0, tk.END)
        final = result["final_mix"]

        # FINAL OUTPUT
        output_text.insert(tk.END, "===== FINAL MIX DESIGN =====\n\n")

        output_text.insert(tk.END, f"{'Target Strength':<22}: {final['target_strength']:.2f} MPa\n")
        output_text.insert(tk.END, f"{'W/C Ratio':<22}: {final['w/c']}\n")
        output_text.insert(tk.END, f"{'Water Content':<22}: {final['water']:.2f} kg/m³\n")
        output_text.insert(tk.END, f"{'Cement Content':<22}: {final['cement']:.2f} kg/m³\n")
        output_text.insert(tk.END, f"{'Coarse Aggregate':<22}: {final['coarse_agg']:.2f} kg/m³\n")
        output_text.insert(tk.END, f"{'Fine Aggregate':<22}: {final['fine_agg']:.2f} kg/m³\n")

        # SUMMARY
        output_text.insert(tk.END, "\n===== SUMMARY =====\n")
        fa_ratio = final['fine_agg'] / final['cement']
        ca_ratio = final['coarse_agg'] / final['cement']
        output_text.insert(tk.END, f"Mix Ratio (C : FA : CA) ≈ 1 : {fa_ratio:.2f} : {ca_ratio:.2f}\n")

        # REMARKS 
        output_text.insert(tk.END, "\n===== ENGINEERING REMARKS =====\n")

        if final["cement"] > 450:
            output_text.insert(tk.END, "⚠ High cement content → consider admixture\n")

        if final["w/c"] < 0.4:
            output_text.insert(tk.END, "✔ Suitable for high strength concrete\n")

        if final["w/c"] > 0.5:
            output_text.insert(tk.END, "⚠ Durability risk due to high w/c ratio\n")

        # TRIAL MIXES
        output_text.insert(tk.END, "\n===== TRIAL MIXES =====\n")

        for i, trial in enumerate(result["trials"]):
            output_text.insert(tk.END, f"\nTrial {i+1}:\n")
            output_text.insert(tk.END, f"  W/C Ratio     : {trial['w/c']}\n")
            output_text.insert(tk.END, f"  Cement        : {trial['cement']} kg/m³\n")
            output_text.insert(tk.END, f"  Coarse Agg    : {trial['coarse_agg']} kg/m³\n")
            output_text.insert(tk.END, f"  Fine Agg      : {trial['fine_agg']} kg/m³\n")

        # ===== RECOMMENDATION =====
        output_text.insert(tk.END, "\n===== RECOMMENDATION =====\n")
        output_text.insert(tk.END, "Final mix should be selected after lab trial validation.\n")

    except Exception as e:
        messagebox.showerror("Error", f"{type(e).__name__}: {e}")


def clear_all():
    output_text.delete(1.0, tk.END)
    grade_var.set("M25")
    exposure_var.set("moderate")
    agg_size_var.set("20")
    slump_var.set("75")
    sand_zone_var.set("Zone II")
    agg_type_var.set("angular")


def save_report():
    file = filedialog.asksaveasfilename(defaultextension=".txt")
    if file:
        with open(file, "w") as f:
            f.write(output_text.get(1.0, tk.END))


# WINDOW 
root = tk.Tk()
root.title("Concrete Mix Design Tool (IS 10262)")
root.geometry("800x720")
root.configure(bg="#eef2f5")

# TITLE 
tk.Label(root, text="Concrete Mix Design Tool",
         font=("Arial", 18, "bold"),
         bg="#eef2f5").pack(pady=10)

# INPUT FRAME 
frame = tk.LabelFrame(root, text="Input Parameters", padx=12, pady=12)
frame.pack(padx=25, pady=15, fill="x")

grade_var = tk.StringVar(value="M25")
exposure_var = tk.StringVar(value="moderate")
agg_size_var = tk.StringVar(value="20")
slump_var = tk.StringVar(value="75")
sand_zone_var = tk.StringVar(value="Zone II")
agg_type_var = tk.StringVar(value="angular")

labels = ["Grade", "Exposure", "Aggregate Size (mm)", "Slump (mm)", "Sand Zone", "Aggregate Type"]

widgets = [
    ttk.Combobox(frame, textvariable=grade_var, values=["M20","M25","M30"]),
    ttk.Combobox(frame, textvariable=exposure_var, values=["mild","moderate","severe"]),
    ttk.Combobox(frame, textvariable=agg_size_var, values=["10","20","40"]),
    tk.Entry(frame, textvariable=slump_var),
    ttk.Combobox(frame, textvariable=sand_zone_var, values=["Zone I","Zone II","Zone III"]),
    ttk.Combobox(frame, textvariable=agg_type_var, values=["angular","sub-angular","rounded"])
]

for i, label in enumerate(labels):
    tk.Label(frame, text=label).grid(row=i, column=0, sticky="w", pady=6)
    widgets[i].grid(row=i, column=1, sticky="ew", pady=6, padx=8)

frame.columnconfigure(1, weight=1)

# BUTTONS 
btn_frame = tk.Frame(root, bg="#eef2f5")
btn_frame.pack(pady=12)

tk.Button(btn_frame, text="Calculate Mix", command=run_calculation,
          bg="#28a745", fg="white", width=20).grid(row=0, column=0, padx=10)

tk.Button(btn_frame, text="Reset", command=clear_all,
          bg="#ffc107", fg="black", width=14).grid(row=0, column=1, padx=10)

tk.Button(btn_frame, text="Save Report", command=save_report,
          bg="#007bff", fg="white", width=16).grid(row=0, column=2, padx=10)

# OUTPUT 
output_frame = tk.LabelFrame(root, text="Results", padx=10, pady=10)
output_frame.pack(padx=25, pady=10, fill="both", expand=True)

output_text = tk.Text(output_frame, wrap="word", font=("Courier New", 10))
output_text.pack(fill="both", expand=True)

root.mainloop()